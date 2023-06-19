/*************************************************************************
 * Clus - Software for Predictive Clustering *
 * Copyright (C) 2007 *
 * Katholieke Universiteit Leuven, Leuven, Belgium *
 * Jozef Stefan Institute, Ljubljana, Slovenia *
 * *
 * This program is free software: you can redistribute it and/or modify *
 * it under the terms of the GNU General Public License as published by *
 * the Free Software Foundation, either version 3 of the License, or *
 * (at your option) any later version. *
 * *
 * This program is distributed in the hope that it will be useful, *
 * but WITHOUT ANY WARRANTY; without even the implied warranty of *
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the *
 * GNU General Public License for more details. *
 * *
 * You should have received a copy of the GNU General Public License *
 * along with this program. If not, see <http://www.gnu.org/licenses/>. *
 * *
 * Contact information: <http://www.cs.kuleuven.be/~dtai/clus/>. *
 *************************************************************************/

package clus.ext.ensembles;

import java.io.FileOutputStream;
import java.io.IOException;
import java.io.OutputStreamWriter;
import java.io.PrintWriter;
import java.util.ArrayList;
import java.util.Arrays;
import java.util.HashMap;
import java.util.Random;
import java.util.concurrent.ExecutionException;
import java.util.concurrent.ExecutorService;
import java.util.concurrent.Executors;
import java.util.concurrent.Future;
import java.util.concurrent.TimeUnit;

import clus.Clus;
import clus.algo.ClusInductionAlgorithm;
import clus.algo.tdidt.ClusDecisionTree;
import clus.algo.tdidt.ClusNode;
import clus.algo.tdidt.DepthFirstInduce;
import clus.algo.tdidt.DepthFirstInduceSparse;
import clus.data.rows.RowData;
import clus.data.rows.TupleIterator;
import clus.data.type.ClusAttrType;
import clus.data.type.ClusSchema;
import clus.error.ClusErrorList;
import clus.error.ComponentError;
import clus.ext.ensembles.containters.OneBagResults;
import clus.ext.ensembles.induceCallables.InduceExtraTreeCallable;
import clus.ext.ensembles.induceCallables.InduceOneBagCallable;
import clus.ext.featureRanking.ClusEnsembleFeatureRanking;
import clus.ext.featureRanking.ClusFeatureRanking;
import clus.heuristic.ClusHeuristic;
import clus.jeans.resource.ResourceInfo;
import clus.main.ClusOutput;
import clus.main.ClusRun;
import clus.main.ClusStatManager;
import clus.main.ClusSummary;
import clus.main.Settings;
import clus.model.ClusModel;
import clus.model.ClusModelInfo;
import clus.model.modelio.ClusModelCollectionIO;
import clus.selection.BaggingSelection;
import clus.selection.OOBSelection;
import clus.statistic.ClusStatistic;
import clus.statistic.ComponentStatistic;
import clus.util.ClusException;
import clus.util.ClusRandom;
import clus.util.ClusRandomNonstatic;
import clus.util.cloner.Cloner;
import clus.util.tools.optimization.GDProbl;


public class ClusEnsembleInduce extends ClusInductionAlgorithm {

    Clus m_BagClus;
    static ClusAttrType[] m_RandomSubspaces; // TODO: this field should be removed in the future
    ClusForest m_OForest;// Forest with the original models
    
    ClusForest[] m_OForests;
    
    ClusForest m_DForest;
    static int m_Mode;

    // Memory optimization
    private static boolean m_OptMode;
    private ClusEnsembleInduceOptimization m_Optimization;
    private ClusEnsembleInduceOptimization[] m_Optimizations;

    // Output ensemble at different values
    int[] m_OutEnsembleAt;// sorted values (ascending)!
    static int m_NbMaxBags;

    // members for target subspacing
    static int m_EnsembleROSScope;
    ClusEnsembleROSInfo m_EnsembleROSInfo;

    // Out-Of-Bag Error Estimate
    ClusOOBErrorEstimate m_OOBEstimation;

    // Feature Ranking via Random Forests OR via Genie3 etc.
    boolean m_FeatRank;
    // ClusEnsembleFeatureRanking m_FeatureRanking;
    ClusEnsembleFeatureRanking[] m_FeatureRankings;

    /** Number of the threads when growing the trees. */
    private int m_NbThreads;


    /**
     * Random tree depths for different iterations, used for tree to rules optimization procedures.
     * This is static because we want different tree depths for different folds.
     */
    // static protected Random m_randTreeDepth = new Random(0);
    
    
    public static final int m_PARALLEL_TRAP_BestFirst_getDescriptiveAttributes = 0;
    public static final int m_PARALLEL_TRAP_DepthFirst_getDescriptiveAttributes = 1;
    public static final int m_PARALLEL_TRAP_staticRandom = 2;
    public static final int m_PARALLEL_TRAP_optimization = 3;
    private static boolean[] m_WarningsGiven = new boolean[4];
    

    public ClusEnsembleInduce(ClusSchema schema, Settings sett, Clus clus) throws ClusException, IOException {
        super(schema, sett);
        initialize(schema, sett, clus);
        sett.updateNbRandomAttrSelected(schema);// moved here because of HSC bug
    }


    // used by FIRE
    public ClusEnsembleInduce(ClusInductionAlgorithm other, Clus clus) throws ClusException, IOException {
        super(other);
        initialize(getSchema(), getSettings(), clus);
        getSettings().updateNbRandomAttrSelected(getSchema());// moved here because of HSC bug
    }


    public void initialize(ClusSchema schema, Settings sett, Clus clus) throws ClusException, IOException {
        m_BagClus = clus;
        m_Mode = ClusStatManager.getMode();
        // optimize if not XVAL and HMC
        m_OptMode = (Settings.shouldOptimizeEnsemble() && ((m_Mode == ClusStatManager.MODE_HIERARCHICAL) || (m_Mode == ClusStatManager.MODE_REGRESSION) || (m_Mode == ClusStatManager.MODE_CLASSIFY)));
        m_EnsembleROSScope = Settings.getEnsembleROSScope();

        // m_OptMode = (Settings.shouldOptimizeEnsemble() && !Settings.IS_XVAL && ((m_Mode ==
        // ClusStatManager.MODE_HIERARCHICAL)||(m_Mode == ClusStatManager.MODE_REGRESSION) || (m_Mode ==
        // ClusStatManager.MODE_CLASSIFY)));
        m_OutEnsembleAt = sett.getNbBaggingSets().getIntVectorSorted();
        m_NbMaxBags = getNbTrees(m_OutEnsembleAt.length - 1);
        m_FeatRank = sett.shouldPerformRanking() && !Settings.IS_XVAL;
        if (m_FeatRank && !Settings.shouldEstimateOOB() && sett.getRankingMethod() == Settings.RANKING_RFOREST) {
            System.err.println("For Feature Ranking RForest, OOB estimate of error should also be performed.");
            System.err.println("OOB Error Estimate is set to true.");
            Settings.m_EnsembleOOBestimate.setValue(true);
        }
        if (Settings.shouldEstimateOOB())
            m_OOBEstimation = new ClusOOBErrorEstimate(m_Mode);
        if (m_FeatRank) {
            if (m_BagClus.getSettings().getSectionMultiLabel().isEnabled()) {
                int[] rankingMeasures = m_BagClus.getSettings().getMultiLabelRankingMeasures();
                if (rankingMeasures.length == 1 && rankingMeasures[0] == Settings.MULTILABEL_MEASURES_ALL) {
                    m_BagClus.getSettings().setToAllMultiLabelRankingMeasures();
                }
            }
            
            // m_FeatureRanking = new ClusFeatureRanking();
                  
            // setNbFeatureRankings(schema, clus.getStatManager());
            //int nbRankings = getNbFeatureRankings();
            //if(getSettings().getVerbose() > 0){
            //	System.out.println("Number of feature rankings computed: " + nbRankings);
            //}
            // m_FeatureRanking.initializeAttributes(schema.getDescriptiveAttributes(), nbRankings);
            // if (sett.getEnsembleMethod() == Settings.ENSEMBLE_EXTRA_TREES){
            // // moj komentar //Dragi comment - take 2
            // if (sett.getRankingMethod() != Settings.RANKING_GENIE3 && sett.getRankingMethod() !=
            // Settings.RANKING_SYMBOLIC){
            // System.err.println("Feature ranking with Extra trees is enabled only with GENIE3 or SYMBOLIC ranking.
            // Setting to GENIE3.");
            // sett.setFeatureRankingMethod(Settings.RANKING_GENIE3);
            // }
            // }
        }
        setNumberOfThreads(sett.getNumberOfThreads());
    }


    /**
     * Sets the number of threads used when inducing an ensemble. If the wanted number of threads
     * ({@code Settings.m_NumberOfThreads}) equals {@code 0}, then all available processors are used.
     * 
     * @param nbThreads
     *        number of threads, greater or equal to {@code 0}.
     */
    public void setNumberOfThreads(int nbThreads) {
        if (nbThreads == 0) {
            m_NbThreads = Runtime.getRuntime().availableProcessors();
        }
        else {
            m_NbThreads = nbThreads;
        }
    }

    
    public void setNbFeatureRankings(ClusSchema schema, ClusStatManager mgr){
        for(int forest = 0; forest < m_FeatureRankings.length; forest++){
        	int nbTrees = getNbTrees(forest);
        	setNbFeatureRankings(m_FeatureRankings[forest], schema, mgr, nbTrees);
        }
    	
    }
    
    /**
     * Sets the number of feature rankings and the ranking description.
     * @param franking
     * @param schema
     * @param mgr
     */
    public void setNbFeatureRankings(ClusEnsembleFeatureRanking franking, ClusSchema schema, ClusStatManager mgr, int nbTrees) {
    	ClusStatistic clusteringStat =  mgr.getStatistic(ClusAttrType.ATTR_USE_CLUSTERING);
    	Settings sett = schema.getSettings();
    	
        int nbRankings = 0;
        ClusAttrType[] clusteringAttrs = schema.getAllAttrUse(ClusAttrType.ATTR_USE_CLUSTERING);
        if(clusteringAttrs.length < 2 && sett.shouldPerformRankingPerTarget()){
        	System.err.println("Situation:");
        	System.err.println("- there is only one clustering attribute");
        	System.err.println("- per target ranking is set to Yes");
        	System.err.println("Consequences:");
        	System.err.println("- per target ranking == overAll ranking");
        	System.err.println("- per target ranking will be set to No");
        	sett.setPerformRankingPerTarget(false);
        }
        ArrayList<String> rankingNames = new ArrayList<String>();
        switch (schema.getSettings().getRankingMethod()) {
            case Settings.RANKING_RFOREST:
            	ClusErrorList errLst = franking.computeErrorList(schema, mgr);            	
            	int nbErrors = errLst.getNbErrors();
            	for(int i = 0; i < nbErrors; i++){
            		nbRankings++; // overall
            		rankingNames.add(String.format("%s:%s", errLst.getError(i).getName(), "overall"));
            		
                    if (sett.shouldPerformRankingPerTarget() && (errLst.getError(i) instanceof ComponentError)){
                    	int nbDim =  errLst.getError(i).getDimension();
                    	nbRankings += nbDim;
                    	for(int j = 0; j < nbDim; j++){
                    		rankingNames.add(String.format("%s:%s", errLst.getError(i).getName(), clusteringAttrs[j].getName()));
                    	}                    	
                    }
            	}
            	franking.setRForestFimpHeader(rankingNames);
                break;
            case Settings.RANKING_GENIE3:
                nbRankings++; // overall
                rankingNames.add(String.format("overAll"));
                if (sett.shouldPerformRankingPerTarget()){
                	if(!(clusteringStat instanceof ComponentStatistic)){
                		System.err.println("Cannot perform per-target ranking for the given type(s) of targets!");
                		System.err.println("This option is now set to false.");
                		sett.setPerformRankingPerTarget(false);
                	}
                	else{
                		int nbComponents = ((ComponentStatistic) clusteringStat).getNbStatisticComponents();
                		nbRankings += nbComponents;
                		for(int j = 0; j < nbComponents; j++){
                			rankingNames.add(String.format("%s", clusteringAttrs[j].getName()));
                		}
                	}
                }
                franking.setGenie3FimpHeader(rankingNames);
                break;
            case Settings.RANKING_SYMBOLIC:
                double[] weights = schema.getSettings().getSymbolicWeights();
                if (weights == null) {
                    weights = new double[] { schema.getSettings().getSymbolicWeight() };
                }
                nbRankings = weights.length;
                franking.setSymbolicFimpHeader(weights);                
                break;
        }
        franking.setNbFeatureRankings(nbRankings);
        int ensType = getSettings().getEnsembleMethod();
        int rankType = getSettings().getRankingMethod();
        franking.setEnsembleRankigDescription(ensType, rankType, nbTrees);
    }

    /**
     * Train a decision tree ensemble with an algorithm given in settings
     * 
     * @throws ClusException,
     *         IOException, InterruptedException
     */
    public void induceAll(ClusRun cr) throws ClusException, IOException, InterruptedException {
        System.out.println("Memory And Time Optimization = " + m_OptMode);
        System.out.println("Out-Of-Bag Estimate of the error = " + Settings.shouldEstimateOOB());
        System.out.println("Perform Feature Ranking = " + m_FeatRank);

        prepareROSEnsemble();
        
        // initialise ranking stuff here: we need stat manager with clustering statistics != null
//        m_FeatureRanking = new ClusEnsembleFeatureRanking();
        m_FeatureRankings = new ClusEnsembleFeatureRanking[m_OutEnsembleAt.length];
        for(int forest = 0; forest < m_FeatureRankings.length; forest++){
        	m_FeatureRankings[forest] = new ClusEnsembleFeatureRanking();
        }
        
        ClusStatManager mgr = getStatManager();
        ClusSchema schema = mgr.getSchema();
//        setNbFeatureRankings(m_FeatureRanking, schema, mgr);
        
        setNbFeatureRankings(schema, mgr);
//        int nbRankings = m_FeatureRanking.getNbFeatureRankings();
        int nbRankings = m_FeatureRankings[0].getNbFeatureRankings();
        for(int forest = 1; forest < m_FeatureRankings.length; forest++){
        	if (m_FeatureRankings[forest].getNbFeatureRankings() != nbRankings){
        		System.err.println("The number of feature rankings should be the same for all forests! Exiting.");
        		System.exit(-1);
        	}
        }
        if(getSettings().getVerbose() > 0){
        	System.out.println("Number of feature rankings computed: " + nbRankings);
        }
        
//        m_FeatureRanking.initializeAttributes(schema.getDescriptiveAttributes(), nbRankings);
        for(int forest = 0; forest < m_FeatureRankings.length; forest++){
        	m_FeatureRankings[forest].initializeAttributes(schema.getDescriptiveAttributes(), nbRankings);
        }
        
        

        m_OForest = new ClusForest(getStatManager(), m_Optimization);  
        m_OForest.addEnsembleROSInfo(m_EnsembleROSInfo);
        
        m_OForests = new ClusForest[m_OutEnsembleAt.length];
        m_Optimizations = new ClusEnsembleInduceOptimization[m_OForests.length];
        for(int i = 0; i < m_OForests.length; i++){
        	m_OForests[i] = new ClusForest(getStatManager(), m_Optimizations[i]);
        	m_OForests[i].addEnsembleROSInfo(m_EnsembleROSInfo);
        }
        
        
        m_DForest = new ClusForest(getStatManager(), m_Optimization);
        TupleIterator train_iterator = null; // = train set iterator
        TupleIterator test_iterator = null; // = test set iterator      

        

        if (m_OptMode) {
            train_iterator = cr.getTrainIter();
            if (cr.getTestIter() != null) {
                test_iterator = cr.getTestSet().getIterator();
            }
            m_Optimization = initializeOptimization(train_iterator, test_iterator);
            m_Optimization.initPredictions(m_OForest.getStat(), m_EnsembleROSInfo);
            m_OForest.setOptimization(m_Optimization);
            for(int i = 0; i < m_Optimizations.length; i++){
            	m_Optimizations[i] = initializeOptimization(train_iterator, test_iterator);
            	m_Optimizations[i].initPredictions(m_OForests[i].getStat(), m_EnsembleROSInfo);
            	m_OForests[i].setOptimization(m_Optimizations[i]);
            }            
            
            m_DForest.setOptimization(m_Optimization);
        }
        
        

        switch (cr.getStatManager().getSettings().getEnsembleMethod()) {
            case Settings.ENSEMBLE_BAGGING: { // Bagging
                System.out.println("Ensemble Method: Bagging");
                induceBagging(cr);
                break;
            }
            case Settings.ENSEMBLE_RFOREST: { // RForest
                System.out.println("Ensemble Method: Random Forest");
                induceBagging(cr);
                break;
            }
            case Settings.ENSEMBLE_RSUBSPACES: { // RSubspaces
                System.out.println("Ensemble Method: Random Subspaces");
                induceSubspaces(cr);
                break;
            }
            case Settings.ENSEMBLE_BAGSUBSPACES: { // Bagging Subspaces
                System.out.println("Ensemble Method: Bagging of Subspaces");
                induceBaggingSubspaces(cr);
                break;
            }
            case Settings.ENSEMBLE_NOBAGRFOREST: { // RForest without bagging (setting: RFeatSelection)
                System.out.println("Ensemble Method: Random Forest without Bagging");
                induceRForestNoBagging(cr);
                break;
            }
            case Settings.ENSEMBLE_PERT: { // PERT in combination with bagging
                System.out.println("Ensemble Method: PERT (in combination with Bagging)");
                induceBagging(cr);
                break;
            }
            case Settings.ENSEMBLE_EXTRA_TREES: { // Extra-Trees ensemble (published by Geurts et al.)
                System.out.println("Ensemble Method: Extra-trees");
                induceExtraTrees(cr);
                break;
            }
        }
        if (m_FeatRank) {
//            m_FeatureRanking.createFimp(cr);
            for(int forest = 0; forest < m_FeatureRankings.length; forest++){
            	m_FeatureRankings[forest].createFimp(cr, String.format("Trees%d", m_OForests[forest].getNbModels()), getNbTrees(forest));
            }
        }
        if (m_OptMode) {
            m_Optimization.roundPredictions();
            for(int i = 0; i < m_Optimizations.length; i++){
            	m_Optimizations[i].roundPredictions();
            }
        }

        postProcessForest(cr);

        // This section is for calculation of the similarity in the ensemble
        // ClusBeamSimilarityOutput bsimout = new ClusBeamSimilarityOutput(cr.getStatManager().getSettings());
        // bsimout.appendToFile(m_OForest.getModels(), cr);
    }


    public ClusModel induceSingleUnpruned(ClusRun cr) throws ClusException, IOException, InterruptedException {
        ClusRun myRun = new ClusRun(cr);
        induceAll(myRun);
        ClusModelInfo info = myRun.getModelInfo(ClusModel.ORIGINAL);
        return info.getModel();
    }


    // this ensemble method builds random forests (i.e. chooses the best test from a subset of attributes at each node),
    // but does not construct bootstrap replicates of the dataset
    public void induceRForestNoBagging(ClusRun cr) throws ClusException, IOException {
        long summ_time = 0; // = ResourceInfo.getTime();
        
        TupleIterator train_iterator = m_OptMode ? cr.getTrainIter() : null; // = train set iterator
        TupleIterator test_iterator = m_OptMode ? cr.getTestIter() :null; // = test set iterator

        Random bagSeedGenerator = new Random(getSettings().getRandomSeed());
        int[] seeds = new int[m_NbMaxBags];
        for (int i = 0; i < m_NbMaxBags; i++) {
            seeds[i] = bagSeedGenerator.nextInt();
        }
        for (int i = 1; i <= m_NbMaxBags; i++) {
            long one_bag_time = ResourceInfo.getTime();
            if (Settings.VERBOSE > 0)
                System.out.println("Bag: " + i);

            ClusRandomNonstatic rnd = new ClusRandomNonstatic(seeds[i - 1]);

            ClusRun crSingle = new ClusRun(cr.getTrainingSet(), cr.getSummary());
            DepthFirstInduce ind;
            if (getSchema().isSparse()) {
                ind = new DepthFirstInduceSparse(this);
            }
            else {
                ind = new DepthFirstInduce(this);
            }
            ind.initialize();
            crSingle.getStatManager().initClusteringWeights();

            ClusModel model = ind.induceSingleUnpruned(crSingle, rnd);
            summ_time += ResourceInfo.getTime() - one_bag_time;
            
            m_OForest.updateCounts((ClusNode) model);
            if (m_OptMode) {
            	m_Optimization.updatePredictionsForTuples(model, train_iterator, test_iterator);
            }
            else {
                m_OForest.addModelToForest(model);
                // ClusModel defmod = ClusDecisionTree.induceDefault(crSingle);
                // m_DForest.addModelToForest(defmod);
            }

            // Valid only when test set is supplied
            if (m_OptMode && (i != m_NbMaxBags) && checkToOutEnsemble(i)) {

//                crSingle.setInductionTime(summ_time);
//                postProcessForest(crSingle);
//                crSingle.setTestSet(cr.getTestIter());
//                crSingle.setTrainingSet(cr.getTrainingSet());
//                outputBetweenForest(crSingle, m_BagClus, "_" + i + "_");
            }
            crSingle.deleteData();
            crSingle.setModels(new ArrayList<ClusModelInfo>());
        }
    }

    public void induceSubspaces(ClusRun cr) throws ClusException, IOException {
        long summ_time = 0; // = ResourceInfo.getTime();
        TupleIterator train_iterator = m_OptMode ? cr.getTrainIter() : null; // = train set iterator
        TupleIterator test_iterator = m_OptMode ? cr.getTestIter() :null; // = test set iterator

        m_OForest.addEnsembleROSInfo(m_EnsembleROSInfo); // TODO: is this (together with the following lines) necessary? see the same lines in induceAll ...
        for(int i = 0; i < m_OForests.length; i++){
        	m_OForests[i].addEnsembleROSInfo(m_EnsembleROSInfo);
        }

        Random bagSeedGenerator = new Random(getSettings().getRandomSeed());
        int[] seeds = new int[m_NbMaxBags];
        for (int i = 0; i < m_NbMaxBags; i++) {
            seeds[i] = bagSeedGenerator.nextInt();
        }
        for (int i = 1; i <= m_NbMaxBags; i++) {
            long one_bag_time = ResourceInfo.getTime();
            if (Settings.VERBOSE > 0)
                System.out.println("Bag: " + i);

            ClusRandomNonstatic rnd = new ClusRandomNonstatic(seeds[i - 1]);

            ClusRun crSingle = new ClusRun(cr.getTrainingSet(), cr.getSummary());
            // parallelisation !!!
            ClusEnsembleInduce.setRandomSubspaces(ClusEnsembleInduce.selectRandomSubspaces(cr.getStatManager().getSchema().getDescriptiveAttributes(), cr.getStatManager().getSettings().getNbRandomAttrSelected(), ClusRandomNonstatic.RANDOM_SELECTION, rnd));
            DepthFirstInduce ind;
            if (getSchema().isSparse()) {
                ind = new DepthFirstInduceSparse(this);
            }
            else {
                ind = new DepthFirstInduce(this);
            }
            ind.initialize();
            crSingle.getStatManager().initClusteringWeights();

            initializeBagROS(crSingle.getStatManager(), i); // this needs to be changed for parallel
                                                                         // implementation

            ClusModel model = ind.induceSingleUnpruned(crSingle, rnd);
            summ_time += ResourceInfo.getTime() - one_bag_time;

            m_OForest.updateCounts((ClusNode) model);
            if (m_OptMode) {
            	m_Optimization.updatePredictionsForTuples(model, train_iterator, test_iterator);
            }
            else {
                m_OForest.addModelToForest(model);
                // ClusModel defmod = ClusDecisionTree.induceDefault(crSingle);
                // m_DForest.addModelToForest(defmod);
            }
            // Valid only when test set is supplied
            if (m_OptMode && (i != m_NbMaxBags) && checkToOutEnsemble(i)) {
//                crSingle.setInductionTime(summ_time);
//                postProcessForest(crSingle);
//                crSingle.setTestSet(cr.getTestIter());
//                crSingle.setTrainingSet(cr.getTrainingSet());
//                outputBetweenForest(crSingle, m_BagClus, "_" + i + "_");
            }
            crSingle.deleteData();
            crSingle.setModels(new ArrayList<ClusModelInfo>());
        }
    }


    public void induceBagging(ClusRun cr) throws ClusException, IOException, InterruptedException {
        int nbrows = cr.getTrainingSet().getNbRows();
        ((RowData) cr.getTrainingSet()).addIndices(); // necessary to be able to print paths
        if ((RowData) cr.getTestSet() != null) {
            ((RowData) cr.getTestSet()).addIndices();
        }

        TupleIterator train_iterator = m_OptMode ? cr.getTrainIter() : null; // = train set iterator
        TupleIterator test_iterator = m_OptMode ? cr.getTestIter() :null; // = test set iterator

        OOBSelection oob_total = null; // = total OOB selection
        OOBSelection oob_sel = null; // = current OOB selection

        m_OForest.addEnsembleROSInfo(m_EnsembleROSInfo);

        // We store the old maxDepth to this if needed. Thus we get the right depth to .out files etc.
        int origMaxDepth = -1;
        if (getSettings().isEnsembleRandomDepth()) {
            // Random depth for the ensembles
            // The original Max depth is used as the average
            origMaxDepth = getSettings().getTreeMaxDepth();
        }
        BaggingSelection msel = null;
        int[] bagSelections = getSettings().getBagSelection().getIntVectorSorted();
        // bagSelections is either -1, 0, a value in [1,Iterations], or 2 values in [1,Iterations]

        Random bagSeedGenerator = new Random(getSettings().getRandomSeed());
        int[] seeds = new int[m_NbMaxBags];
        for (int i = 0; i < m_NbMaxBags; i++) {
            seeds[i] = bagSeedGenerator.nextInt();
        }

        Cloner cloner = new Cloner();
        ClusStatManager[] statManagerClones = new ClusStatManager[m_NbMaxBags];
        for (int i = 0; i < statManagerClones.length; i++) {
            statManagerClones[i] = cloner.deepClone(cr.getStatManager()); // must be cloned here
        }

        ExecutorService executor = Executors.newFixedThreadPool(m_NbThreads);
        ArrayList<Future<OneBagResults>> bagResults = new ArrayList<Future<OneBagResults>>();

        if (bagSelections[0] == -1) {
            // normal bagging procedure
            for (int i = 1; i <= m_NbMaxBags; i++) {
                ClusRandomNonstatic rnd = new ClusRandomNonstatic(seeds[i - 1]);

                msel = new BaggingSelection(nbrows, getSettings().getEnsembleBagSize(), rnd);
                if (Settings.shouldEstimateOOB()) { // OOB estimate is on
                    // TODO: synchronisation
                    oob_sel = new OOBSelection(msel);
                    if (i == 1) { // initialization
                        oob_total = new OOBSelection(msel);
                    }
                    else {
                        oob_total.addToThis(oob_sel);
                    }
                }
                OOBSelection current_oob_total = cloner.deepClone(oob_total);
                // induceOneBag(cr, i, origMaxDepth, oob_sel, oob_total, train_iterator, test_iterator, msel, rnd);
                InduceOneBagCallable worker = new InduceOneBagCallable(this, cr, i, origMaxDepth, oob_sel, current_oob_total, train_iterator, test_iterator, msel, rnd, statManagerClones[i - 1]); 
                Future<OneBagResults> submit = executor.submit(worker);
                bagResults.add(submit);
            }
        }
        else if (bagSelections[0] == 0) {
            // we assume that files _bagI.model exist, for I=1..m_NbMaxBags and build the forest from them
            makeForestFromBags(cr, train_iterator, test_iterator);
        }
        else {
            // only one or a range of bags needs to be computed (and the model output) e.g. because we want to run the
            // forest in parallel,
            // or because we want to add a number of trees to an existing forest.
            for (int i = 1; i < bagSelections[0]; i++) {
                // we eventually want the same bags as when computing them sequentially.
                msel = new BaggingSelection(nbrows, getSettings().getEnsembleBagSize(), null); // not really necessary any more
            }
            for (int i = bagSelections[0]; i <= bagSelections[1]; i++) {
                ClusRandomNonstatic rnd = new ClusRandomNonstatic(seeds[i - 1]);
                msel = new BaggingSelection(nbrows, getSettings().getEnsembleBagSize(), rnd);
                if (Settings.shouldEstimateOOB()) { // OOB estimate is on
                    oob_sel = new OOBSelection(msel);
                }
                // induceOneBag(cr, i, origMaxDepth, oob_sel, oob_total, train_iterator, test_iterator, msel, rnd);
                InduceOneBagCallable worker = new InduceOneBagCallable(this, cr, i, origMaxDepth, oob_sel, oob_total, train_iterator, test_iterator, msel, rnd, cloner.deepClone(cr.getStatManager()));
                Future<OneBagResults> submit = executor.submit(worker);
                bagResults.add(submit);
            }
        }

        executor.shutdown();
        executor.awaitTermination(Integer.MAX_VALUE, TimeUnit.SECONDS);

        for (int i = 1; i <= bagResults.size(); i++) { // must start with 1 and end with the size
            Future<OneBagResults> future = bagResults.get(i - 1);
            try {
                OneBagResults results = future.get();
                if(!m_OptMode){
                	updateForests(results.getModel(), i);
                }
                if (getSettings().shouldPerformRanking()) {
                    updateFeatureRankings(i, results.getFimportances());
                }

                ClusRun crSingle = results.getSingleRun();
                // Lines that are commented out in this if-section are already executed in induceOneBag
                if (checkToOutEnsemble(i) && (getSettings().getBagSelection().getIntVectorSorted()[0] == -1)) {
                    // crSingle.setInductionTime(m_SummTime);

                    postProcessForest(crSingle);
                    if (Settings.shouldEstimateOOB()) {
                        if (i == m_NbMaxBags) {
                            m_OOBEstimation.postProcessForestForOOBEstimate(crSingle, oob_total, (RowData) cr.getTrainingSet(), m_BagClus, "");
                        }
                        else {
                            m_OOBEstimation.postProcessForestForOOBEstimate(crSingle, oob_total, (RowData) cr.getTrainingSet(), m_BagClus, "_" + i + "_");
                        }
                    }

                    // if (m_OptMode && (i != m_NbMaxBags)){
                    // crSingle.setTestSet(cr.getTestIter());
                    // crSingle.setTrainingSet(cr.getTrainingSet());
                    // outputBetweenForest(crSingle, m_BagClus, "_"+ i +"_");
                    // }
                }

            }
            catch (InterruptedException e) {
                e.printStackTrace();
                System.exit(-1);
            }
            catch (ExecutionException e) {
                e.printStackTrace();
                System.exit(-1);
            }
        }

        // Restore the old maxDepth
        if (origMaxDepth != -1) {
            getSettings().setTreeMaxDepth(origMaxDepth);
        }

    }


    /**
     * Method for generating ROS ensemble subspaces
     * 
     * @param ClusSchema
     *        schema
     * @param sizeOfSubspace
     *        size of subspace
     * @return ClusEnsembleROSInfo object with created subspaces
     */
    static ClusEnsembleROSInfo generateROSEnsembleSubspaces(ClusSchema schema, int sizeOfSubspace) {
        int cnt = m_NbMaxBags;
        int[] enabled;
        ArrayList<int[]> subspaces = new ArrayList<int[]>();

        boolean isRandom = sizeOfSubspace <= 0;
        int subspaceCount = sizeOfSubspace;

        // find indices of target and clustering attributes
        int[] targetIDs = new int[schema.getNbTargetAttributes()];
        int[] clusteringIDs = new int[schema.getNbAllAttrUse(ClusAttrType.ATTR_USE_CLUSTERING)];

        ClusAttrType[] targets = schema.getTargetAttributes();
        ClusAttrType[] clustering = schema.getAllAttrUse(ClusAttrType.ATTR_USE_CLUSTERING);

        for (int t = 0; t < targetIDs.length; t++)
            targetIDs[t] = targets[t].getIndex();
        for (int t = 0; t < clusteringIDs.length; t++)
            clusteringIDs[t] = clustering[t].getIndex();

        // create subspaces
        while (cnt > 1) {
            enabled = new int[schema.getNbAttributes()];

            // enable all attributes
            Arrays.fill(enabled, 1);

            // disable all targets
            for (int i = 0; i < targets.length; i++)
                enabled[targets[i].getIndex()] = 0;

            // if number of randomly selected targets should also be randomized
            if (isRandom)
                subspaceCount = ClusRandom.nextInt(ClusRandom.RANDOM_ENSEMBLE_ROS_SUBSPACE_SIZE_SELECTION, 1, targets.length); // use a separate randomizer for randomized target subspace size selection

            // randomly select targets
            ClusAttrType[] selected = selectRandomSubspaces(targets, subspaceCount, ClusRandom.RANDOM_ENSEMBLE_ROS, null); // inject ClusRandom.RANDOM_ENSEMBLE_TARGET_SUBSPACING randomizer

            // enable selected targets
            for (int i = 0; i < selected.length; i++)
                enabled[selected[i].getIndex()] = 1;

            // safety check: check if at least one target attr is enabled
            int sum = 0;
            for (int a = 0; a < targetIDs.length; a++)
                sum += enabled[targetIDs[a]];
            if (sum > 0) {
                // check if at least one clustering attr is enabled
                sum = 0;
                for (int a = 0; a < clusteringIDs.length; a++)
                    sum += enabled[clusteringIDs[a]];
                if (sum > 0) {
                    subspaces.add(enabled); // subspace meets the criteria, add it to the list
                    cnt--;
                }
            }
        }

        // create one MT model for all targets
        enabled = new int[schema.getNbAttributes()];
        Arrays.fill(enabled, 1); // enable all attributes
        subspaces.add(enabled);

        return new ClusEnsembleROSInfo(schema, subspaces);
    } 
     

    /**
     * Preparation for ROS ensembles
     */
    void prepareROSEnsemble() {
        if (Settings.isEnsembleROSEnabled()) {
            if (getSettings().getEnsembleMethod() != Settings.ENSEMBLE_BAGGING && getSettings().getEnsembleMethod() != Settings.ENSEMBLE_RFOREST && getSettings().getEnsembleMethod() != Settings.ENSEMBLE_RSUBSPACES && getSettings().getEnsembleMethod() != Settings.ENSEMBLE_EXTRA_TREES)

                throw new RuntimeException("ROS extension is not implemented for the selected ensemble method!");

            if (Settings.VERBOSE > 1)
                System.out.println("ROS: creating target subspaces.");

            int subspaceSize = getSettings().calculateNbRandomAttrSelected(getSchema(), 2);

            m_EnsembleROSInfo = generateROSEnsembleSubspaces(getSchema(), subspaceSize);
        }
    }


    void initializeBagROS(ClusStatManager mgr, int bagNo) throws ClusException {
        if (Settings.isEnsembleROSEnabled()) {

            // get heuristic in use
            ClusHeuristic h = mgr.getHeuristic();

            // check if the attribute weights are set
            if (h.getClusteringAttributeWeights() == null)
                throw new RuntimeException("Heuristic does not support ROS!");

            // get subspace of targets that we have previously prepared
            boolean[] enabled = m_EnsembleROSInfo.getModelSubspaceBoolean(bagNo - 1);

            // push to already initialized heuristic
            h.setClusteringWeightsEnabledAttributes(enabled);

            // display info of the targets, that are being used
            if (getSettings().getVerbose() >= 1) {
                int[] trgts = m_EnsembleROSInfo.getOnlyTargets(m_EnsembleROSInfo.getModelSubspace(bagNo - 1));

                if (trgts.length > 15) {
                    System.err.println("Enabled targets: " + ClusEnsembleROSInfo.getEnabledCount(trgts) + " of " + trgts.length);
                }
                else {
                    System.err.println("Enabled targets: " + Arrays.toString(trgts));
                }
            }
        }
    }


    public OneBagResults induceOneBag(ClusRun cr, int i, int origMaxDepth, OOBSelection oob_sel, OOBSelection oob_total, TupleIterator train_iterator, TupleIterator test_iterator, BaggingSelection msel, ClusRandomNonstatic rnd, ClusStatManager mgr) throws ClusException, IOException, InterruptedException {
        long one_bag_time = ResourceInfo.getTime();
        if (Settings.VERBOSE > 0)
            System.out.println("Bag: " + i);

        if (getSettings().isEnsembleRandomDepth()) {
            // Set random tree max depth
            getSettings().setTreeMaxDepth(GDProbl.randDepthWighExponentialDistribution(
                    // m_randTreeDepth.nextDouble(),
                    rnd.nextDouble(ClusRandomNonstatic.RANDOM_INT_RANFOR_TREE_DEPTH), origMaxDepth));
        }

        ClusRun crSingle = m_BagClus.partitionDataBasic(cr.getTrainingSet(), msel, cr.getSummary(), i);

        DepthFirstInduce ind;

        // ordinary bagging run
        if (getSchema().isSparse()) {
            ind = new DepthFirstInduceSparse(this, mgr, true);
        }
        else {
            ind = new DepthFirstInduce(this, mgr, true);
        }

        ind.initialize();

        crSingle.getStatManager().initClusteringWeights(); // TODO: when using rules: if (checkToOutEnsemble(i) && (getSettings().getBagSelection().getIntVectorSorted()[0] == -1)) ----> postprocess... To we need more than one stat manager?
        ind.getStatManager().initClusteringWeights(); // equivalent to mgr.initClusteringWeights();

        initializeBagROS(ind.getStatManager(), i);

        ClusModel model = ind.induceSingleUnpruned(crSingle, rnd);
        //m_SummTime += ResourceInfo.getTime() - one_bag_time;
        one_bag_time = ResourceInfo.getTime() - one_bag_time;
        
//        int[] additionalModelsNodesLeaves = m_OForest.updateCounts((ClusNode) model);
//        for(int ii = m_OForests.length - 1; ii >= 0; ii--){
//        	if (getNbTrees(ii) >= i){
//        		m_OForests[ii].updateCounts(additionalModelsNodesLeaves[0], additionalModelsNodesLeaves[1], additionalModelsNodesLeaves[2]);
//        	} else{
//        		break;        		
//        	}
//        }
        updateCounts((ClusNode) model, i);

        // OOB estimate for the parallel implementation is done in makeForestFromBags method <--- matejp: This is some
        // old parallelisation
        if (Settings.shouldEstimateOOB() && (getSettings().getBagSelection().getIntVectorSorted()[0] == -1)) {
            m_OOBEstimation.updateOOBTuples(oob_sel, (RowData) cr.getTrainingSet(), model);
        }

        HashMap<String, double[][]> fimportances = new HashMap<String, double[][]>();
        if (m_FeatRank) {// franking
        	// this suffices even in the case when we grow more than one forest 
            if (m_BagClus.getSettings().getRankingMethod() == Settings.RANKING_RFOREST) {
                fimportances = m_FeatureRankings[0].calculateRFimportance(model, cr, oob_sel, rnd, ind.getStatManager());
            }
            else if (m_BagClus.getSettings().getRankingMethod() == Settings.RANKING_GENIE3) {
                // m_FeatureRanking.calculateGENIE3importance((ClusNode)model, cr);
                fimportances = m_FeatureRankings[0].calculateGENIE3importanceIteratively((ClusNode) model, ind.getStatManager());
            }
            else if (m_BagClus.getSettings().getRankingMethod() == Settings.RANKING_SYMBOLIC) {
                double[] weights = m_BagClus.getSettings().getSymbolicWeights();
                if (weights == null) {
                    weights = new double[] { m_BagClus.getSettings().getSymbolicWeight() };
                }
                // m_FeatureRanking.calculateSYMBOLICimportance((ClusNode)model, weights, 0);
                fimportances = m_FeatureRankings[0].calculateSYMBOLICimportanceIteratively((ClusNode) model, weights);
            }
        }
        boolean canForgetTheRun = true;
        if (m_OptMode) {
//        	m_Optimization.updatePredictionsForTuples(model, train_iterator, test_iterator);
        	updatePredictionsForTuples(model, train_iterator, test_iterator, i);
            model = null;
        }
        // instead of adding the model here, we will do this in after all bags are completed to keep the order of the
        // models invariant
        // else{
        // m_OForest.addModelToForest(model);

        // this was commented out before parallelism ClusModel defmod = ClusDecisionTree.induceDefault(crSingle);
        // this was commented out before parallelism m_DForest.addModelToForest(defmod);
        // }

        // printing paths taken by each example in each tree (used in ICDM'11 paper on "Random forest based feature
        // induction")
        if (getSettings().isPrintEnsemblePaths()) {
            PrintWriter pw = new PrintWriter(new OutputStreamWriter(new FileOutputStream("tree_" + i + ".path")));
            ((ClusNode) model).numberCompleteTree();
            ((ClusNode) model).printPaths(pw, "", "", (RowData) cr.getTrainingSet(), oob_sel, false);
            if ((RowData) cr.getTestSet() != null) {
                ((ClusNode) model).printPaths(pw, "", "", (RowData) cr.getTestSet(), null, true);
            }
        }

        // Valid only when test set is supplied
        if (checkToOutEnsemble(i) && (getSettings().getBagSelection().getIntVectorSorted()[0] == -1)) {
            //crSingle.setInductionTime(m_SummTime);
            crSingle.setInductionTime(one_bag_time);
            canForgetTheRun = false;

            // Lines that are commented out are executed AT THE END of induceBagging

            // postProcessForest(crSingle);
            // if (Settings.shouldEstimateOOB()){
            // if (i == m_NbMaxBags){
            // m_OOBEstimation.postProcessForestForOOBEstimate(crSingle, oob_total, (RowData)cr.getTrainingSet(),
            // m_BagClus, "");
            // } else{
            // m_OOBEstimation.postProcessForestForOOBEstimate(crSingle, oob_total, (RowData)cr.getTrainingSet(),
            // m_BagClus, "_"+ i +"_");
            // }
            // }
            //
            if (m_OptMode && (i != m_NbMaxBags)) {
            	if(m_NbThreads > 1){
            		giveParallelisationWarning(ClusEnsembleInduce.m_PARALLEL_TRAP_optimization);
            	}
//                crSingle.setTestSet(cr.getTestIter());
//                crSingle.setTrainingSet(cr.getTrainingSet());
//                outputBetweenForest(crSingle, m_BagClus, "_" + i + "_");
            }
        }

        if ((getSettings().getBagSelection().getIntVectorSorted()[0] != -1) || (getSettings().isPrintEnsembleModelFiles())) {
            ClusModelCollectionIO io = new ClusModelCollectionIO();
            ClusModelInfo orig_info = crSingle.addModelInfo("Original");
            orig_info.setModel(model);
            m_BagClus.saveModels(crSingle, io);
            io.save(m_BagClus.getSettings().getFileAbsolute(cr.getStatManager().getSettings().getAppName() + "_bag" + i + ".model"));
        }

        if (canForgetTheRun) {
            crSingle.deleteData();
            crSingle.setModels(new ArrayList<ClusModelInfo>());
        }

        return new OneBagResults(model, fimportances, crSingle, oob_total, one_bag_time);
    }


    public void makeForestFromBags(ClusRun cr, TupleIterator train_iterator, TupleIterator test_iterator) throws ClusException, IOException {
        try {
            OOBSelection oob_total = null; // = total OOB selection
            OOBSelection oob_sel = null; // = current OOB selection
            BaggingSelection msel = null;
            System.out.println("Start loading models");

            Random bagSeedGenerator = new Random(getSettings().getRandomSeed());
            int[] seeds = new int[m_NbMaxBags];
            for (int i = 0; i < m_NbMaxBags; i++) {
                seeds[i] = bagSeedGenerator.nextInt();
            }
            for (int i = 1; i <= m_NbMaxBags; i++) {
                System.out.println("Loading model for bag " + i);
                ClusRandomNonstatic rnd = new ClusRandomNonstatic(seeds[i - 1]);

                ClusModelCollectionIO io = ClusModelCollectionIO.load(m_BagClus.getSettings().getFileAbsolute(getSettings().getAppName() + "_bag" + i + ".model"));
                ClusModel orig_bag_model = io.getModel("Original");
                if (orig_bag_model == null) { throw new ClusException(cr.getStatManager().getSettings().getAppName() + "_bag" + i + ".model file does not contain model named 'Original'"); }
                
                m_OForest.updateCounts((ClusNode) orig_bag_model);
                if (m_OptMode) {
                	m_Optimization.updatePredictionsForTuples(orig_bag_model, train_iterator, test_iterator);
                }
                else {
                    m_OForest.addModelToForest(orig_bag_model);
                }
                if (Settings.shouldEstimateOOB()) { // OOB estimate is on
                    // the same bags will be generated for the corresponding models!!!
                    msel = new BaggingSelection(cr.getTrainingSet().getNbRows(), getSettings().getEnsembleBagSize(), rnd);
                    oob_sel = new OOBSelection(msel);
                    if (i == 1) { // initialization
                        oob_total = new OOBSelection(msel);
                    }
                    else
                        oob_total.addToThis(oob_sel);
                    m_OOBEstimation.updateOOBTuples(oob_sel, (RowData) cr.getTrainingSet(), orig_bag_model);
                }

                if (checkToOutEnsemble(i)) {
                    postProcessForest(cr);
                    if (Settings.shouldEstimateOOB()) {
                        if (i == m_NbMaxBags)
                            m_OOBEstimation.postProcessForestForOOBEstimate(cr, oob_total, (RowData) cr.getTrainingSet(), m_BagClus, "");
                        else
                            m_OOBEstimation.postProcessForestForOOBEstimate(cr, oob_total, (RowData) cr.getTrainingSet(), m_BagClus, "_" + i + "_");
                    }
                    if (m_OptMode && i != m_NbMaxBags) {
//                        outputBetweenForest(cr, m_BagClus, "_" + i + "_");
                    }
                }
                cr.setModels(new ArrayList<ClusModelInfo>());// do not store the models

                // Dragi, IJS - we don't store the predictions of the default models
                /*
                 * ClusModel def_bag_model = io.getModel("Default");
                 * if (def_bag_model == null) {
                 * throw new ClusException(cr.getStatManager().getSettings().getAppName() + "_bag" + i +
                 * ".model file does not contain model named 'Default'");
                 * }
                 * m_DForest.addModelToForest(def_bag_model);
                 */
            }
        }
        catch (ClassNotFoundException e) {
            throw new ClusException("Error: not all of the _bagX.model files were found");
        }
    }


    public void induceBaggingSubspaces(ClusRun cr) throws ClusException, IOException {
        int nbrows = cr.getTrainingSet().getNbRows();

        long summ_time = 0; // = ResourceInfo.getTime();

        TupleIterator train_iterator = m_OptMode ? cr.getTrainIter() : null; // = train set iterator
        TupleIterator test_iterator = m_OptMode ? cr.getTestIter() :null; // = test set iterator
        
        OOBSelection oob_total = null; // = total OOB selection
        OOBSelection oob_sel = null; // = current OOB selection

        Random bagSeedGenerator = new Random(getSettings().getRandomSeed());
        int[] seeds = new int[m_NbMaxBags];
        for (int i = 0; i < m_NbMaxBags; i++) {
            seeds[i] = bagSeedGenerator.nextInt();
        }
        for (int i = 1; i <= m_NbMaxBags; i++) {
            long one_bag_time = ResourceInfo.getTime();
            if (Settings.VERBOSE > 0)
                System.out.println("Bag: " + i);

            ClusRandomNonstatic rnd = new ClusRandomNonstatic(seeds[i - 1]);
            BaggingSelection msel = new BaggingSelection(nbrows, getSettings().getEnsembleBagSize(), rnd);

            ClusRun crSingle = m_BagClus.partitionDataBasic(cr.getTrainingSet(), msel, cr.getSummary(), i);
            // parallelisation !!!
            ClusEnsembleInduce.setRandomSubspaces(ClusEnsembleInduce.selectRandomSubspaces(cr.getStatManager().getSchema().getDescriptiveAttributes(), cr.getStatManager().getSettings().getNbRandomAttrSelected(), ClusRandomNonstatic.RANDOM_SELECTION, rnd));
            DepthFirstInduce ind;
            if (getSchema().isSparse()) {
                ind = new DepthFirstInduceSparse(this);
            }
            else {
                ind = new DepthFirstInduce(this);
            }
            ind.initialize();

            crSingle.getStatManager().initClusteringWeights();
            ind.initializeHeuristic();

            ClusModel model = ind.induceSingleUnpruned(crSingle, rnd);
            summ_time += ResourceInfo.getTime() - one_bag_time;

            m_OForest.updateCounts((ClusNode) model);
            if (Settings.shouldEstimateOOB()) { // OOB estimate is on
                oob_sel = new OOBSelection(msel);
                if (i == 1)
                    oob_total = new OOBSelection(msel);
                else
                    oob_total.addToThis(oob_sel);
                m_OOBEstimation.updateOOBTuples(oob_sel, (RowData) cr.getTrainingSet(), model);
            }

            if (m_OptMode) {
            	m_Optimization.updatePredictionsForTuples(model, train_iterator, test_iterator);
            }
            else {
                m_OForest.addModelToForest(model);
                ClusModel defmod = ClusDecisionTree.induceDefault(crSingle);
                m_DForest.addModelToForest(defmod);
            }

            if (checkToOutEnsemble(i)) {
                crSingle.setInductionTime(summ_time);
                postProcessForest(crSingle);
                if (Settings.shouldEstimateOOB()) {
                    if (i == m_NbMaxBags)
                        m_OOBEstimation.postProcessForestForOOBEstimate(crSingle, oob_total, (RowData) cr.getTrainingSet(), m_BagClus, "");
                    else
                        m_OOBEstimation.postProcessForestForOOBEstimate(crSingle, oob_total, (RowData) cr.getTrainingSet(), m_BagClus, "_" + i + "_");
                }
                if (m_OptMode && (i != m_NbMaxBags)) {
//                    crSingle.setTestSet(cr.getTestIter());
//                    crSingle.setTrainingSet(cr.getTrainingSet());
//                    outputBetweenForest(crSingle, m_BagClus, "_" + i + "_");
                }
            }
            crSingle.deleteData();
            crSingle.setModels(new ArrayList<ClusModelInfo>());
        }
    }


    public void induceExtraTrees(ClusRun cr) throws ClusException, IOException, InterruptedException {
        long indTimeSequential = 0;
        
        TupleIterator train_iterator = m_OptMode ? cr.getTrainIter() : null; // = train set iterator
        TupleIterator test_iterator = m_OptMode ? cr.getTestIter() : null; // = test set iterator

        m_OForest.addEnsembleROSInfo(m_EnsembleROSInfo);

        Random bagSeedGenerator = new Random(getSettings().getRandomSeed());
        int[] seeds = new int[m_NbMaxBags];
        for (int i = 0; i < m_NbMaxBags; i++) {
            seeds[i] = bagSeedGenerator.nextInt();
        }

        Cloner cloner = new Cloner();
        ClusStatManager[] statManagerClones = new ClusStatManager[m_NbMaxBags];
        for (int i = 0; i < statManagerClones.length; i++) {
            statManagerClones[i] = cloner.deepClone(cr.getStatManager()); // must be cloned here
        }

        ExecutorService executor = Executors.newFixedThreadPool(m_NbThreads);
        ArrayList<Future<OneBagResults>> bagResults = new ArrayList<Future<OneBagResults>>();

        for (int i = 1; i <= m_NbMaxBags; i++) {
            ClusRandomNonstatic rnd = new ClusRandomNonstatic(seeds[i - 1]);
            InduceExtraTreeCallable worker = new InduceExtraTreeCallable(this, cr, i, train_iterator, test_iterator, rnd, statManagerClones[i - 1]); // <-- induceExtraTree(cr, i, train_iterator, test_iterator, rnd, summ_time, one_bag_time, statManagerClones[i - 1]);
            Future<OneBagResults> submit = executor.submit(worker);
            bagResults.add(submit);
        }

        executor.shutdown();
        executor.awaitTermination(Integer.MAX_VALUE, TimeUnit.SECONDS);

        for (int i = 1; i <= bagResults.size(); i++) { // must start with 1 and end with the size
            Future<OneBagResults> future = bagResults.get(i - 1);
            try {
                OneBagResults results = future.get();
                
                if (!m_OptMode){
                	updateForests(results.getModel(), i);
                } 
                if (getSettings().shouldPerformRanking()) {
                	// m_FeatureRanking.putAttributesInfos(results.getFimportances());
                	updateFeatureRankings(i, results.getFimportances());
                    
                }
                
                indTimeSequential += results.getInductionTime();
            }
            catch (InterruptedException e) {
                e.printStackTrace();
                System.exit(-1);
            }
            catch (ExecutionException e) {
                e.printStackTrace();
                System.exit(-1);
            }
        }
        
        cr.setInductionTimeSequential(indTimeSequential);

    }

    public OneBagResults induceOneExtraTree(ClusRun cr, int i, TupleIterator train_iterator, TupleIterator test_iterator, ClusRandomNonstatic rnd, ClusStatManager mgr) throws ClusException, IOException, InterruptedException {
        long one_bag_time = ResourceInfo.getTime();
        if (Settings.VERBOSE > 0)
            System.out.println("Bag: " + i);

        ClusRun crSingle = new ClusRun(cr.getTrainingSet(), cr.getSummary());
        // ClusEnsembleInduce.setRandomSubspaces(cr.getStatManager().getSchema().getDescriptiveAttributes(),
        // cr.getStatManager().getSettings().getNbRandomAttrSelected());
        DepthFirstInduce ind;
        if (getSchema().isSparse()) {
            ind = new DepthFirstInduceSparse(this, mgr, true);
        }
        else {
            ind = new DepthFirstInduce(this, mgr, true);
        }
               
        ind.initialize();
        crSingle.getStatManager().initClusteringWeights();
        ind.getStatManager().initClusteringWeights();

        initializeBagROS(ind.getStatManager(), i);
       
        
        ClusModel model = ind.induceSingleUnpruned(crSingle, rnd);
      
        one_bag_time = ResourceInfo.getTime() - one_bag_time;

//        int[] additionalModelsNodesLeaves = m_OForest.updateCounts((ClusNode) model);
//        for(int ii = m_OForests.length - 1; ii >= 0; ii--){
//        	if (getNbTrees(ii) >= i){
//        		m_OForests[ii].updateCounts(additionalModelsNodesLeaves[0], additionalModelsNodesLeaves[1], additionalModelsNodesLeaves[2]);
//        	} else{
//        		break;        		
//        	}
//        }
        updateCounts((ClusNode) model, i);

        HashMap<String, double[][]> fimportances = new HashMap<String, double[][]>();
        if (m_FeatRank) {// franking genie3
            // if (m_BagClus.getSettings().getRankingMethod() == Settings.RANKING_RFOREST)
            // m_FeatureRanking.calculateRFimportance(model, cr, oob_sel);
            if (m_BagClus.getSettings().getRankingMethod() == Settings.RANKING_GENIE3) {
                // m_FeatureRanking.calculateGENIE3importance((ClusNode)model, cr);
                fimportances = m_FeatureRankings[0].calculateGENIE3importanceIteratively((ClusNode) model, ind.getStatManager());
            }

            else if (m_BagClus.getSettings().getRankingMethod() == Settings.RANKING_SYMBOLIC) {
                double[] weights = m_BagClus.getSettings().getSymbolicWeights();
                if (weights == null) {
                    weights = new double[] { m_BagClus.getSettings().getSymbolicWeight() };
                }
                // m_FeatureRanking.calculateSYMBOLICimportance((ClusNode)model, weights, 0);
                fimportances = m_FeatureRankings[0].calculateSYMBOLICimportanceIteratively((ClusNode) model, weights);
            }
            else {
                System.err.println("The following feature ranking methods are implemented for Extra trees:");
                System.err.println("Genie3");
                System.err.println("Symbolic");
                System.err.println("But you have chosen ranking method " + Settings.RANKING_TYPE[m_BagClus.getSettings().getRankingMethod()]);
                System.err.println("No ranking will be computed.");
                m_FeatRank = false;

            }
        }
        
        if (m_OptMode) {
        	updatePredictionsForTuples(model, train_iterator, test_iterator, i);
        	// m_Optimization.updatePredictionsForTuples(model, train_iterator, test_iterator);        	
        	model = null;
        }
        else {
            // m_OForest.addModelToForest(model); <-- THIS IS DONE IN induceExtraTrees

            // ClusModel defmod = ClusDecisionTree.induceDefault(crSingle);
            // m_DForest.addModelToForest(defmod);
        }

        // Valid only when test set is supplied
        if (m_OptMode && (i != m_NbMaxBags) && checkToOutEnsemble(i)) {
        	if (m_NbThreads > 1){
        		giveParallelisationWarning(ClusEnsembleInduce.m_PARALLEL_TRAP_optimization);
        	}
//            crSingle.setInductionTime(one_bag_time);
//            postProcessForest(crSingle);
//            crSingle.setTestSet(cr.getTestIter());
//            crSingle.setTrainingSet(cr.getTrainingSet());
//            outputBetweenForest(crSingle, m_BagClus, "_" + i + "_");
        }

        crSingle.deleteData();
        crSingle.setModels(new ArrayList<ClusModelInfo>());

        return new OneBagResults(model, fimportances, crSingle, null, one_bag_time);
    }


    // Checks whether we reached a limit
    public boolean checkToOutEnsemble(int idx) {
        for (int i = 0; i < m_OutEnsembleAt.length; i++)
            if (m_OutEnsembleAt[i] == idx)
                return true;
        return false;
    }


    public void postProcessForest(ClusRun cr) throws ClusException {
        ClusModelInfo def_info = cr.addModelInfo("Default");
        if (m_OptMode)
            m_DForest = null;
        def_info.setModel(ClusDecisionTree.induceDefault(cr));

        ClusModelInfo orig_info = cr.addModelInfo("Original");
        orig_info.setModel(m_OForest);
        
        for(int i = 0; i < m_OForests.length; i++){
        	int nbTrees = m_OForests[i].getNbModels();
        	ClusModelInfo moj_info = cr.addModelInfo(String.format("Forest with %d tree%s", nbTrees, nbTrees == 1 ? "" : "s"));
        	moj_info.setModel(m_OForests[i]);
        }

        // Application of Thresholds for HMC
        if (ClusStatManager.getMode() == ClusStatManager.MODE_HIERARCHICAL) {
            double[] thresholds = cr.getStatManager().getSettings().getClassificationThresholds().getDoubleVector();
            // setting the printing preferences in the HMC mode
            m_OForest.setPrintModels(Settings.isPrintEnsembleModels());
            if (!m_OptMode)
                m_DForest.setPrintModels(Settings.isPrintEnsembleModels());
            if (thresholds != null) {
                for (int i = 0; i < thresholds.length; i++) {
                    ClusModelInfo pruned_info = cr.addModelInfo("T(" + thresholds[i] + ")");
                    ClusForest new_forest = m_OForest.cloneForestWithThreshold(thresholds[i]);
                    new_forest.setPrintModels(Settings.isPrintEnsembleModels());
                    pruned_info.setShouldWritePredictions(false);
                    pruned_info.setModel(new_forest);
                }
            }
        }

        // If we want to convert trees to rules but not use
        // any of the rule learning tehniques anymore (if CoveringMethod != RulesFromTree)
        if (getSettings().rulesFromTree() != Settings.CONVERT_RULES_NONE && getSettings().getCoveringMethod() != Settings.COVERING_METHOD_RULES_FROM_TREE) {
            m_OForest.convertToRules(cr, false);
        }
    }


    public synchronized void outputBetweenForest(ClusRun cr, Clus cl, String addname) throws IOException, ClusException {
        // if (m_OptMode){
        // ClusEnsembleInduceOptimization.roundPredictions();
        // }
        Settings sett = cr.getStatManager().getSettings();
        ClusSchema schema = cr.getStatManager().getSchema();
        ClusOutput output = new ClusOutput(sett.getAppName() + addname + ".out", schema, sett);
        ClusSummary summary = cr.getSummary();
        getStatManager().computeTrainSetStat((RowData) cr.getTrainingSet());
        cl.calcError(cr, null, null); // Calc error
        if (summary != null) {
            for (int i = ClusModel.ORIGINAL; i < cr.getNbModels(); i++) {
                ClusModelInfo summ_info = cr.getModelInfo(i);
                ClusErrorList test_err = summ_info.getTestError();
                summ_info.setTestError(test_err);
            }
        }
        cl.calcExtraTrainingSetErrors(cr);
        output.writeHeader();
        output.writeOutput(cr, true, getSettings().isOutTrainError());
        output.close();
        cl.getClassifier().saveInformation(sett.getAppName());
        ClusModelCollectionIO io = new ClusModelCollectionIO();
        cl.saveModels(cr, io);
        io.save(cl.getSettings().getFileAbsolute(cr.getStatManager().getSettings().getAppName() + addname + ".model"));
    }


    /**
     * Maximum number of bags for memory optimization
     */
    public static int getMaxNbBags() {
        return ClusEnsembleInduce.m_NbMaxBags;
    }
    
    public int getNbTrees(int forestIndex){
    	return m_OutEnsembleAt[forestIndex];
    }


    /**
     * Selects random subspaces.
     * 
     * @param attrs
     *        -- For which attributes
     * @param select
     *        -- How many
     */
    public static ClusAttrType[] selectRandomSubspaces(ClusAttrType[] attrs, int select, int randomizerVersion, ClusRandomNonstatic rand) {
        int origsize = attrs.length;
        int[] samples = new int[origsize];
        int rnd;
        boolean randomize = true;
        int i = 0;
        if (rand == null) {
            while (randomize) {
                rnd = ClusRandom.nextInt(randomizerVersion, origsize);
                if (samples[rnd] == 0) {
                    samples[rnd]++;
                    i++;
                }
                randomize = i != select;
            }
        }
        else {
            while (randomize) {
                rnd = rand.nextInt(randomizerVersion, origsize);
                if (samples[rnd] == 0) {
                    samples[rnd]++;
                    i++;
                }
                randomize = i != select;
            }
        }

        ClusAttrType[] result = new ClusAttrType[select];
        int res = 0;
        for (int k = 0; k < origsize; k++) {
            if (samples[k] != 0) {
                result[res] = attrs[k];
                res++;
            }
        }
        return result;
    }


    public static ClusAttrType[] getRandomSubspaces() {
        return m_RandomSubspaces;
    }

    public static void setRandomSubspaces(ClusAttrType[] attrs){
    	m_RandomSubspaces = attrs;
    }
    
//    public static void setRandomSubspaces(ClusAttrType[] attrs, int select, ClusRandomNonstatic rnd) {
//        m_RandomSubspaces = ClusEnsembleInduce.selectRandomSubspaces(attrs, select, ClusRandomNonstatic.RANDOM_SELECTION, rnd);
//    }


    /**
     * Memory optimization
     */
    public static boolean isOptimized() {
        return m_OptMode;
    }


    public ClusFeatureRanking getEnsembleFeatureRanking(int i) {
        return m_FeatureRankings[i];
    }
    
    public synchronized static void giveParallelisationWarning(int reason){
    	if (!m_WarningsGiven[reason]){
    		String message;
    		switch (reason){
    		case ClusEnsembleInduce.m_PARALLEL_TRAP_BestFirst_getDescriptiveAttributes:
    			message = "clus.ext.bestfirst.BestFirstInduce.getDescriptiveAttributes() has been called. This may not work in parallel setting.";
    			break;
    		case ClusEnsembleInduce.m_PARALLEL_TRAP_DepthFirst_getDescriptiveAttributes:
    			message = "clus.algo.tdidt.DepthFirstInduce.getDescriptiveAttributes(ClusRandomNonstatic) has been called. This may not work in parallel setting.";
    			break;
    		case ClusEnsembleInduce.m_PARALLEL_TRAP_staticRandom:
    			message = "Static random has been called. This may not work in parallel setting.";
    			break;
    		case ClusEnsembleInduce.m_PARALLEL_TRAP_optimization:
    			message = "Memory usage optimization is on. You have reached a place where there might be some unexpected behaviour in parallel setting because of that.";
    			break;
    		default:
    			throw new RuntimeException("Wrong reason for giveParallelisationWarning: " + reason);
    		}
    		System.err.println("Warning:");
    		System.err.println(message);
    		System.err.println("There will be no additional warnings for this.");
    		m_WarningsGiven[reason] = true;
    		
    	}
    }
    
    /**
     * Updates the counts of nodes, leaves and trees in the forests, by adding the corresponding statistics
     * of a new tree to the current statistics in forest.
     * @param model
     * @param treeNumber
     */
    private void updateCounts(ClusNode model, int treeNumber){
        int[] additionalModelsNodesLeaves = m_OForest.updateCounts((ClusNode) model);
        for(int ii = m_OForests.length - 1; ii >= 0; ii--){
        	if (getNbTrees(ii) >= treeNumber){
        		m_OForests[ii].updateCounts(additionalModelsNodesLeaves[0], additionalModelsNodesLeaves[1], additionalModelsNodesLeaves[2]);
        	} else{
        		break;        		
        	}
        }
    }
    
    /**
     * Updated the feature ranking importances for all rankings, by adding the importances from a new tree.
     * @param treeIndex
     * @param fimportances
     * @throws InterruptedException
     */
    private void updateFeatureRankings(int treeIndex, HashMap<String, double[][]> fimportances) throws InterruptedException {
//    	m_FeatureRanking.putAttributesInfos(fimportances);
    	for(int forest = m_OForests.length - 1; forest >= 0; forest--){
    		if (getNbTrees(forest) >= treeIndex){
    			m_FeatureRankings[forest].putAttributesInfos(fimportances);
    		} else{
    			break;
    		}
    	}
	}
    
    /**
     * Updates the forests by adding a new tree.
     * @param model
     * @param treeNumber
     */
    private void updateForests(ClusModel model, int treeNumber) {
    	m_OForest.addModelToForest(model);
    	for(int forest = m_OForests.length - 1; forest >= 0; forest--){
    		if (getNbTrees(forest) >= treeNumber){
    			m_OForests[forest].addModelToForest(model);
    		} else{
    			break;
    		}
    	}
	}
    
    private ClusEnsembleInduceOptimization initializeOptimization(TupleIterator train_iterator, TupleIterator test_iterator) throws IOException, ClusException{
        if (m_Mode == ClusStatManager.MODE_HIERARCHICAL || m_Mode == ClusStatManager.MODE_REGRESSION){
        	return new ClusEnsembleInduceOptRegHMLC(train_iterator, test_iterator);
        } else if (m_Mode == ClusStatManager.MODE_CLASSIFY){
        	return new ClusEnsembleInduceOptClassification(train_iterator, test_iterator);
        } else{
        	int[] values = new int[]{ClusStatManager.MODE_HIERARCHICAL, ClusStatManager.MODE_REGRESSION, ClusStatManager.MODE_CLASSIFY, m_Mode};
        	String line1 = "Optimization supported only for the following modes:";
        	String line2 = String.format("MODE_HIERARCHICAL = %d, MODE_REGRESSION = %d and MODE_CLASSIFY = %d", values[0], values[1], values[2]);
        	String line3 = String.format("Unfortunately: m_Mode = %d", values[3]);
        	String message = String.join("\n", line1, line2, line3);
        	throw new ClusException(message);
        }
        // old version: additional argument in constructors:
        // test_iterator != null ? cr.getTrainingSet().getNbRows() + cr.getTestSet().getNbRows()) : cr.getTrainingSet().getNbRows();
    }
    
    private void updatePredictionsForTuples(ClusModel model, TupleIterator train_iterator, TupleIterator test_iterator, int treeNumber) throws IOException, ClusException{
    	m_Optimization.updatePredictionsForTuples(model, train_iterator, test_iterator);
    	for(int forest = m_OForests.length - 1; forest >= 0; forest--){
    		if (getNbTrees(forest) >= treeNumber){
    			m_Optimizations[forest].updatePredictionsForTuples(model, train_iterator, test_iterator);
    		} else{
    			break;
    		}
    	}
    }

}
