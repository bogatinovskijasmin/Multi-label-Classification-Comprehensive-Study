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

package clus.algo.kNN;

import java.io.IOException;
import java.io.PrintWriter;
import java.io.Serializable;
import java.util.ArrayList;
import java.util.Arrays;
import java.util.HashMap;
import java.util.LinkedList;

import clus.algo.kNN.distance.ChebyshevDistance;
import clus.algo.kNN.distance.EuclideanDistance;
import clus.algo.kNN.distance.ManhattanDistance;
import clus.algo.kNN.distance.SearchDistance;
import clus.algo.kNN.distance.attributeWeighting.AttributeWeighting;
import clus.algo.kNN.distance.attributeWeighting.NoWeighting;
import clus.algo.kNN.distance.attributeWeighting.RandomForestWeighting;
import clus.algo.kNN.distance.attributeWeighting.UserDefinedWeighting;
import clus.algo.kNN.distance.distanceWeighting.DistanceWeighting;
import clus.algo.kNN.distance.distanceWeighting.WeightConstant;
import clus.algo.kNN.distance.distanceWeighting.WeightMinus;
import clus.algo.kNN.distance.distanceWeighting.WeightOver;
import clus.algo.kNN.methods.SearchAlgorithm;
import clus.algo.kNN.methods.bfMethod.BrutForce;
import clus.algo.kNN.methods.kdTree.KDTree;
import clus.algo.kNN.methods.vpTree.VPTree;
import clus.data.rows.DataTuple;
import clus.data.rows.RowData;
import clus.data.type.ClusAttrType;
import clus.data.type.ClusSchema;
import clus.data.type.NumericAttrType;
import clus.ext.hierarchical.WHTDStatistic;
import clus.ext.timeseries.TimeSeriesStat;
import clus.jeans.util.MyArray;
import clus.main.ClusModelInfoList;
import clus.main.ClusRun;
import clus.main.Settings;
import clus.model.ClusModel;
import clus.statistic.ClusDistance;
import clus.statistic.ClusStatistic;
import clus.statistic.StatisticPrintInfo;
import clus.util.ClusException;
import com.google.gson.JsonObject;


/**
 *
 * @author Mitja Pugelj
 */
public class KnnModel implements ClusModel, Serializable {

    private static final long serialVersionUID = Settings.SERIAL_VERSION_ID;
    public static final int WEIGHTING_CONSTANT = 1; // 1
    public static final int WEIGHTING_INVERSE = 2; // d^{-1}
    public static final int WEIGHTING_MINUS = 3; // 1-d

    private SearchAlgorithm search;
    private int weightingOption;
    private ClusRun cr;
    protected ClusStatistic statTemplate;
    private int m_K = 1; // the number of nearest neighbours, see also https://www.youtube.com/watch?v=KqOsrniBooQ
    private int m_MaxK = 1; // maximal number of neighbours among the master itself and his 'workeks': for efficient use
                            // of predictWeighted in Clus.calcError()
    private DataTuple m_CurrentTuple; // used for efficient use of predictWeighted in Clus.calcError()
    private LinkedList<DataTuple> m_CurrentNeighbours; // m_MaxK nearest neighbours of m_CurrentTuple
    private KnnModel m_Master = null;


    // Slave mode - this model is used only for voting, searching is done by master
    public KnnModel(ClusRun cr, int k, int weighting, KnnModel master) {
        this.cr = cr;
        this.m_K = k;
        this.m_MaxK = Math.max(this.m_K, master.m_MaxK);
        master.m_MaxK = this.m_MaxK;
        this.weightingOption = weighting;
        this.search = master.search;
        this.statTemplate = master.statTemplate;
        this.m_Master = master;
    }


    // Default constructor.
    public KnnModel(ClusRun cr, int k, int weighting) throws ClusException, IOException {
        this.cr = cr;
        this.m_K = k;
        this.m_MaxK = Math.max(this.m_K, this.m_MaxK);
        this.weightingOption = weighting;
        // settings file name; use name for .weight file
        String fName = this.cr.getStatManager().getSettings().getAppName();
        // Initialize attribute weighting according to settings file
        AttributeWeighting attrWe = new NoWeighting();
        ;
        String attrWeighting = Settings.kNN_attrWeight.getStringValue();
        boolean loadedWeighting = false;
        if (attrWeighting.toLowerCase().compareTo("none") == 0) {

        }
        else if (attrWeighting.startsWith("RF")) {
            try {
                String[] wS = attrWeighting.split(",");
                int nbBags = 100; // Default value
                if (wS.length == 2)
                    nbBags = Integer.parseInt(wS[1]);
                else
                    Settings.kNN_attrWeight.setValue(attrWeighting + "," + nbBags);
                attrWe = new RandomForestWeighting(this.cr, nbBags);
            }
            catch (Exception e) {
                throw new ClusException("Error at reading attributeWeighting value. RF value detected, but error accured while reading number of bags.");
            }
        }
        else if (attrWeighting.startsWith("[") && attrWeighting.endsWith("]")) {
            try {
                String[] wS = attrWeighting.substring(1, attrWeighting.length() - 1).split(",");
                double[] we = new double[wS.length];
                for (int i = 0; i < we.length; i++)
                    we[i] = Double.parseDouble(wS[i]);
                attrWe = new UserDefinedWeighting(we);
            }
            catch (Exception e) {
                throw new ClusException("Error at reading attributeWeighting value. User defined entry detected, but value cannot be red..");
            }

        }
        else {
            // Probably file name.. try to load weighting.
            attrWe = AttributeWeighting.loadFromFile(fName + ".weight");
            System.out.println(attrWe.toString());
            if (attrWe != null)
                loadedWeighting = true;
            else
                throw new ClusException("Unrecognized attributeWeighting value (" + attrWeighting + ")");
        }

        if (!(attrWe instanceof NoWeighting) && !loadedWeighting) {
            AttributeWeighting.saveToFile(attrWe, fName + ".weight");
        }

        // Initialize distance according to settings file
        String dist = Settings.kNN_distance.getStringValue();
        SearchDistance searchDistance = new SearchDistance();
        ClusDistance distance;

        if (dist.toLowerCase().compareTo("chebyshev") == 0) {
            distance = new ChebyshevDistance(searchDistance);
        }
        else if (dist.toLowerCase().compareTo("manhattan") == 0) {
            distance = new ManhattanDistance(searchDistance);
        }
        else {
            distance = new EuclideanDistance(searchDistance);
        }

        // initialize min values of numeric attributes: needed for normalization in the distance computation
        int[] data_types = new int[] { ClusModelInfoList.TRAINSET, ClusModelInfoList.TESTSET, ClusModelInfoList.VALIDATIONSET };
        double[] mins = null;
        double[] maxs = null;
        int nb_attrs = -1;
        for (int type = 0; type < data_types.length; type++) {
            RowData data = cr.getDataSet(type);
            ClusSchema schema = cr.getStatManager().getSchema();
            if (data != null) {
                if (mins == null) {
                    nb_attrs = schema.getNbAttributes();
                    mins = new double[nb_attrs];
                    Arrays.fill(mins, Double.POSITIVE_INFINITY);
                    maxs = new double[nb_attrs];
                    Arrays.fill(maxs, Double.NEGATIVE_INFINITY);
                }
                // compute max and min for every numeric attribute
                for (int tuple_ind = 0; tuple_ind < data.getNbRows(); tuple_ind++) {
                    for (int i = 0; i < nb_attrs; i++) {
                        ClusAttrType attr_type = schema.getAttrType(i);
                        if (!attr_type.isDisabled() && attr_type instanceof NumericAttrType) {
                            double t = attr_type.getNumeric(data.getTuple(tuple_ind));
                            if (t < mins[i] && t != Double.POSITIVE_INFINITY) {
                                mins[i] = t;
                            }
                            if (t > maxs[i] && t != Double.POSITIVE_INFINITY) {
                                maxs[i] = t;
                            }
                        }
                    }

                }
            }
        }

        searchDistance.setDistance(distance);
        distance.setWeighting(attrWe);
        searchDistance.setNormalizationWeights(mins, maxs);

        // Select search method according to settings file.
        String alg = Settings.kNN_method.getStringValue();
        if (alg.compareTo("vp-tree") == 0) {
            this.search = new VPTree(this.cr, searchDistance);
        }
        else if (alg.compareTo("kd-tree") == 0) {
            this.search = new KDTree(this.cr, searchDistance);
        }
        else {
            this.search = new BrutForce(this.cr, searchDistance);
        }

        // debug info
        System.out.println("------------------------------------------------");
        System.out.println(this.search.getClass());
        System.out.println(searchDistance.getBasicDistance().getClass());
        System.out.println(this.m_K);
        System.out.println(Settings.kNN_distanceWeight.getStringValue());
        System.out.println("------------------------------------------------");

        // build tree, preprocessing
        this.search.build();

        // save prediction template
        // @todo : should all this be repalced with:
        statTemplate = cr.getStatManager().getStatistic(ClusAttrType.ATTR_USE_TARGET);

        // if( cr.getStatManager().getMode() == ClusStatManager.MODE_CLASSIFY ){
        // if(cr.getStatManager().getSettings().getSectionMultiLabel().isEnabled()){
        // statTemplate = new
        // ClassificationStat(this.cr.getDataSet(ClusRun.TRAINSET).m_Schema.getNominalAttrUse(ClusAttrType.ATTR_USE_TARGET),
        // cr.getStatManager().getSettings().getMultiLabelTrheshold());
        // } else{
        // statTemplate = new
        // ClassificationStat(this.cr.getDataSet(ClusRun.TRAINSET).m_Schema.getNominalAttrUse(ClusAttrType.ATTR_USE_TARGET));
        // }
        // }
        // else if( cr.getStatManager().getMode() == ClusStatManager.MODE_REGRESSION )
        // statTemplate = new
        // RegressionStat(this.cr.getDataSet(ClusRun.TRAINSET).m_Schema.getNumericAttrUse(ClusAttrType.ATTR_USE_TARGET));
        // else if( cr.getStatManager().getMode() == ClusStatManager.MODE_TIME_SERIES ){
        // // TimeSeriesAttrType attr =
        // this.cr.getDataSet(ClusRun.TRAINSET).m_Schema.getTimeSeriesAttrUse(ClusAttrType.ATTR_USE_TARGET)[0];
        // // statTemplate = new TimeSeriesStat(attxr, new DTWTimeSeriesDist(attr), 0 );
        // System.out.println("-------------");
        // statTemplate = cr.getStatManager().getStatistic(ClusAttrType.ATTR_USE_TARGET);
        // System.out.println(statTemplate.getDistanceName());
        // System.out.println("----------------");
        // }else if( cr.getStatManager().getMode() == ClusStatManager.MODE_HIERARCHICAL ){
        // statTemplate = cr.getStatManager().getStatistic(ClusAttrType.ATTR_USE_TARGET);
        // System.out.println("----------------------");
        // System.out.println(statTemplate.getDistanceName());
        // System.out.println(statTemplate.getClass());
        // System.out.println("----------------------");
        // }
    }


    public ClusStatistic predictWeighted(DataTuple tuple) {
        LinkedList<DataTuple> nearest = new LinkedList<DataTuple>(); // the first m_K neigbhours of the m_MaxK
                                                                     // neighbours: OK, because the neighbours are
                                                                     // sorted from the nearest to the farthest

        if (this.m_Master == null) { // this is the master
            this.m_CurrentNeighbours = this.search.returnNNs(tuple, this.m_MaxK);
            this.m_CurrentTuple = tuple;
            for (int neighbour = 0; neighbour < this.m_K; neighbour++) {
                nearest.add(this.m_CurrentNeighbours.get(neighbour));
            }
        }
        else { // this is a slave
            if (this.m_Master.m_CurrentTuple != tuple) { throw new RuntimeException("The neighbours were computed for tuple\n" + this.m_Master.m_CurrentTuple.toString() + "\nbut now, we are dealing with tuple\n" + tuple.toString()); }
            for (int neighbour = 0; neighbour < this.m_K; neighbour++) {
                nearest.add(this.m_Master.m_CurrentNeighbours.get(neighbour));
            }
        }

        // Initialize distance weighting according to setting file
        DistanceWeighting weighting;
        if (this.weightingOption == WEIGHTING_INVERSE) {
            weighting = new WeightOver(nearest, this.search, tuple);
        }
        else if (this.weightingOption == WEIGHTING_MINUS) {
            weighting = new WeightMinus(nearest, this.search, tuple);
        }
        else {
            weighting = new WeightConstant(nearest, this.search, tuple);
        }
        // Vote
        ClusStatistic stat = statTemplate.cloneStat();
        if (stat instanceof TimeSeriesStat) {
            for (DataTuple dt : nearest) {
                ClusStatistic dtStat = statTemplate.cloneStat();
                dtStat.setSDataSize(1);
                dtStat.updateWeighted(dt, 0);
                dtStat.computePrediction();
                stat.addPrediction(dtStat, weighting.weight(dt));
            }
            stat.computePrediction();
        }
        else if (stat instanceof WHTDStatistic) {
            for (DataTuple dt : nearest)
                stat.updateWeighted(dt, weighting.weight(dt));
            stat.calcMean();
        }
        else {
            for (DataTuple dt : nearest)
                stat.updateWeighted(dt, weighting.weight(dt));
            stat.calcMean();
        }
        return stat;
    }


    public void applyModelProcessors(DataTuple tuple, MyArray mproc) throws IOException {
        System.out.println("-----------");
    }


    public int getModelSize() {
        System.out.println("No specific model size for kNN model.");
        return -1;
    }


    public String getModelInfo() {
        return "kNN model weighted with " + this.weightingOption + " and " + m_K + " neighbors.";
    }


    public void printModel(PrintWriter wrt) {
        wrt.println("No specific kNN model to write!");
    }


    public void printModel(PrintWriter wrt, StatisticPrintInfo info) {
        wrt.println("No specific kNN model to write!");
        wrt.print(info.toString());
    }


    public void printModelAndExamples(PrintWriter wrt, StatisticPrintInfo info, RowData examples) {
        throw new UnsupportedOperationException(this.getClass().getName() + ":printModelAndExamples() - Not supported yet for kNN.");
    }


    public void printModelToQuery(PrintWriter wrt, ClusRun cr, int starttree, int startitem, boolean exhaustive) {
        throw new UnsupportedOperationException(this.getClass().getName() + ":printModelToQuery() - Not supported yet for kNN.");
    }


    public void printModelToPythonScript(PrintWriter wrt) {
        throw new UnsupportedOperationException(this.getClass().getName() + ":printModelToPythonScript() - Not supported yet for kNN.");
    }

    @Override
    public JsonObject getModelJSON() {
        return null;
    }

    @Override
    public JsonObject getModelJSON(StatisticPrintInfo info) {
        return null;
    }

    @Override
    public JsonObject getModelJSON(StatisticPrintInfo info, RowData examples) {
        return null;
    }


    public void attachModel(HashMap table) throws ClusException {
        throw new UnsupportedOperationException(this.getClass().getName() + ":attachModel - Not supported yet for kNN.");
    }


    public void retrieveStatistics(ArrayList list) {
        throw new UnsupportedOperationException(this.getClass().getName() + ":retrieveStatistics - Not supported yet for kNN.");
    }


    public ClusModel prune(int prunetype) {
        throw new UnsupportedOperationException(this.getClass().getName() + ":prune - Not supported yet for kNN.");
    }


    public int getID() {
        throw new UnsupportedOperationException(this.getClass().getName() + ":getID - Not supported yet for kNN.");
    }

}
