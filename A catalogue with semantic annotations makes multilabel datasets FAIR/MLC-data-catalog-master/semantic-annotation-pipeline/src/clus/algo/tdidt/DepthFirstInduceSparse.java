
package clus.algo.tdidt;

import java.io.IOException;
import java.util.ArrayList;

import clus.algo.ClusInductionAlgorithm;
import clus.algo.split.CurrentBestTestAndHeuristic;
import clus.algo.split.NominalSplit;
import clus.data.rows.RowData;
import clus.data.rows.SparseDataTuple;
import clus.data.type.ClusAttrType;
import clus.data.type.ClusSchema;
import clus.data.type.NominalAttrType;
import clus.data.type.NumericAttrType;
import clus.data.type.SparseNumericAttrType;
import clus.main.ClusStatManager;
import clus.main.Settings;
import clus.model.test.NodeTest;
import clus.util.ClusException;
import clus.util.ClusRandomNonstatic;


public class DepthFirstInduceSparse extends DepthFirstInduce {

    public DepthFirstInduceSparse(ClusSchema schema, Settings sett) throws ClusException, IOException {
        super(schema, sett);
        if (Settings.VERBOSE > 0)
            System.out.println("Sparse implementation");
    }


    public DepthFirstInduceSparse(ClusInductionAlgorithm other) {
        super(other);
        if (Settings.VERBOSE > 0)
            System.out.println("Sparse implementation");
    }


    public DepthFirstInduceSparse(ClusInductionAlgorithm other, NominalSplit split) {
        super(other);
        if (Settings.VERBOSE > 0)
            System.out.println("Sparse implementation");
    }


    /**
     * Used in parallelisation.
     * 
     * @param other
     * @param mgr
     * @param parallelism
     *        Used only to distinguish between this constructor and
     *        {@code DepthFirstInduce(ClusInductionAlgorithm, NominalSplit)}, when the second argument is {@code null}.
     */
    public DepthFirstInduceSparse(ClusInductionAlgorithm other, ClusStatManager mgr, boolean parallelism) {
        super(other, mgr, parallelism);
        if (Settings.VERBOSE > 0)
            System.out.println("Sparse implementation");
    }


    public void initializeExamples(ClusAttrType[] attrs, RowData data) {
        // first remove all examplelists from attributes (-> ensembles!)
        for (int i = 0; i < attrs.length; i++) {
            ClusAttrType at = attrs[i];
            if (at.isSparse()) {
                ((SparseNumericAttrType) at).resetExamples();
            }
        }

        for (int i = 0; i < data.getNbRows(); i++) {
            SparseDataTuple tuple = (SparseDataTuple) data.getTuple(i);
            tuple.addExampleToAttributes();
        }
    }


    public void induce(ClusNode node, RowData data, ClusRandomNonstatic rnd) {
        if (getSettings().isEnsembleMode() && ((getSettings().getEnsembleMethod() == Settings.ENSEMBLE_RFOREST) || (getSettings().getEnsembleMethod() == Settings.ENSEMBLE_NOBAGRFOREST))) {
            induceRandomForest(node, data, rnd);
        }
        else {
            ClusAttrType[] attrs = getDescriptiveAttributes(rnd);
            initializeExamples(attrs, data);
            ArrayList<ClusAttrType> attrList = new ArrayList<ClusAttrType>();
            // ArrayList<ArrayList<SparseDataTuple>> examplelistList = new ArrayList<ArrayList<SparseDataTuple>>();
            for (int i = 0; i < attrs.length; i++) {
                ClusAttrType at = attrs[i];
                if (at.isSparse()) {
                    if (((SparseNumericAttrType) at).getExampleWeight() >= getSettings().getMinimalWeight()) {
                        attrList.add(at);

                        // Object[] exampleArray = ((SparseNumericAttrType) at).getExamples().toArray(); // tuples with non-zero value for this attribute
                        // RowData exampleData = new RowData(exampleArray, exampleArray.length);

                        // exampleData.sortSparse((SparseNumericAttrType) at, m_FindBestTest.getSortHelper());

                        // ArrayList<SparseDataTuple> exampleList = new ArrayList<SparseDataTuple>(); // tuples, sorted in descending order by at.value
                        // for (int j = 0; j < exampleData.getNbRows(); j++) {
                        //     exampleList.add((SparseDataTuple) exampleData.getTuple(j));
                        // }
                        // ((SparseNumericAttrType) at).setExamples(exampleList);
                        // examplelistList.add(exampleList);
                    }
                }
                else {
                    attrList.add(at);
                    // examplelistList.add(null);
                }
            }
            Object[] attrArray = attrList.toArray();
            // Object[] examplelistArray = examplelistList.toArray();
            induce(node, data, attrArray, rnd);//, examplelistArray);
        }
    }


    public void induce(ClusNode node, RowData data, Object[] attrs, ClusRandomNonstatic rnd) { // , Object[] examplelists
        // System.out.println("INDUCE SPARSE with " + attrs.length + " attributes and " + data.getNbRows() + "
        // examples");
        // Initialize selector and perform various stopping criteria
        if (initSelectorAndStopCrit(node, data)) {
            makeLeaf(node);
            return;
        }
        // Find best test
        for (int i = 0; i < attrs.length; i++) {
            ClusAttrType at = (ClusAttrType) attrs[i];
            // ArrayList examplelist = (ArrayList) examplelists[i];
            if (at.isNominal()){ // at instanceof NominalAttrType
            	m_FindBestTest.findNominal((NominalAttrType) at, data, rnd);
            }
            // else if (examplelist == null) {
            //    m_FindBestTest.findNumeric((NumericAttrType) at, data, null);
            // }
            else {
                m_FindBestTest.findNumeric((NumericAttrType) at, data, rnd);//examplelist);
            }
        }

        // Partition data + recursive calls
        CurrentBestTestAndHeuristic best = m_FindBestTest.getBestTest();
        if (best.hasBestTest()) {
            node.testToNode(best);
            // Output best test
            if (Settings.VERBOSE > 1)
                System.out.println("Test: " + node.getTestString() + " -> " + best.getHeuristicValue());
            // Create children
            int arity = node.updateArity();
            NodeTest test = node.getTest();
            RowData[] subsets = new RowData[arity];
            for (int j = 0; j < arity; j++) {
                subsets[j] = data.applyWeighted(test, j);
            }
            if (getSettings().showAlternativeSplits()) {
                filterAlternativeSplits(node, data, subsets);
            }
            if (node != m_Root && getSettings().hasTreeOptimize(Settings.TREE_OPTIMIZE_NO_INODE_STATS)) {
                // Don't remove statistics of root node; code below depends on them
                node.setClusteringStat(null);
                node.setTargetStat(null);
            }

            for (int j = 0; j < arity; j++) {
                ClusNode child = new ClusNode();
                node.setChild(child, j);
                child.initClusteringStat(m_StatManager, m_Root.getClusteringStat(), subsets[j]);
                child.initTargetStat(m_StatManager, m_Root.getTargetStat(), subsets[j]);
                ArrayList<ClusAttrType> attrList = new ArrayList<ClusAttrType>();
                // ArrayList<ArrayList> examplelistList = new ArrayList<ArrayList>();
                for (int i = 0; i < attrs.length; i++) {
                    ClusAttrType at = (ClusAttrType) attrs[i];
                    if (at.isSparse()) {
                        ArrayList<SparseDataTuple> newExampleList = ((SparseNumericAttrType) at).pruneExampleList(subsets[j]);
                        double exampleWeight = getExampleWeight(newExampleList);
                        if (exampleWeight >= getSettings().getMinimalWeight()) {
                            attrList.add(at);
                            // examplelistList.add(newExampleList);
                        }
                    }
                    else {
                        attrList.add(at);
                        // examplelistList.add(null);
                    }
                }
                Object[] attrArray = attrList.toArray();
                // Object[] exampleListArray = examplelistList.toArray();
                induce(child, subsets[j], attrArray, rnd);//exampleListArray);
            }
        }
        else {
            makeLeaf(node);
        }
    }


    public double getExampleWeight(ArrayList examples) {
        double weight = 0.0;
        for (int i = 0; i < examples.size(); i++) {
            SparseDataTuple tup = (SparseDataTuple) examples.get(i);
            weight += tup.getWeight();
        }
        return weight;
    }


    // for random forests, a different induce approach is taken, because at each node, we have a different set of
    // attributes
    public void induceRandomForest(ClusNode node, RowData data, ClusRandomNonstatic rnd) {
        ClusAttrType[] attrs = getSchema().getDescriptiveAttributes();
        initializeExamples(attrs, data);
        induceRandomForestRecursive(node, data, rnd);
    }


    public void induceRandomForestRecursive(ClusNode node, RowData data, ClusRandomNonstatic rnd) {
        ClusAttrType[] attrs = getDescriptiveAttributes(rnd);
        ArrayList<ClusAttrType> attrList = new ArrayList<ClusAttrType>();
        for (int i = 0; i < attrs.length; i++) {
            ClusAttrType at = attrs[i];
            if (at.isSparse()) {
                if (((SparseNumericAttrType) at).getExampleWeight() >= getSettings().getMinimalWeight()) {
                    attrList.add(at);
                }
            }
            else {
                attrList.add(at);
            }
        }
        Object[] attrArray = attrList.toArray();
        induceRandomForestRecursive2(node, data, attrArray, rnd);

    }


    public void induceRandomForestRecursive2(ClusNode node, RowData data, Object[] attrs, ClusRandomNonstatic rnd) {
        // System.out.println("INDUCE SPARSE with " + attrs.length + " attributes and " + data.getNbRows() + "
        // examples");
        // Initialize selector and perform various stopping criteria
        if (initSelectorAndStopCrit(node, data)) {
            makeLeaf(node);
            return;
        }
        // Find best test
        for (int i = 0; i < attrs.length; i++) {
            ClusAttrType at = (ClusAttrType) attrs[i];
            if (at.isNominal()) // at instanceof NominalAttrType
                m_FindBestTest.findNominal((NominalAttrType) at, data, rnd);
            else
                m_FindBestTest.findNumeric((NumericAttrType) at, data, rnd);
        }

        // Partition data + recursive calls
        CurrentBestTestAndHeuristic best = m_FindBestTest.getBestTest();
        if (best.hasBestTest()) {
            node.testToNode(best);
            // Output best test
            if (Settings.VERBOSE > 1)
                System.out.println("Test: " + node.getTestString() + " -> " + best.getHeuristicValue());
            // Create children
            int arity = node.updateArity();
            NodeTest test = node.getTest();
            RowData[] subsets = new RowData[arity];
            for (int j = 0; j < arity; j++) {
                subsets[j] = data.applyWeighted(test, j);
            }
            if (getSettings().showAlternativeSplits()) {
                filterAlternativeSplits(node, data, subsets);
            }
            if (node != m_Root && getSettings().hasTreeOptimize(Settings.TREE_OPTIMIZE_NO_INODE_STATS)) {
                // Don't remove statistics of root node; code below depends on them
                node.setClusteringStat(null);
                node.setTargetStat(null);
            }

            for (int j = 0; j < arity; j++) {
                ClusNode child = new ClusNode();
                node.setChild(child, j);
                child.initClusteringStat(m_StatManager, m_Root.getClusteringStat(), subsets[j]);
                child.initTargetStat(m_StatManager, m_Root.getTargetStat(), subsets[j]);

                induceRandomForestRecursive(child, subsets[j], rnd);
            }
        }
        else {
            makeLeaf(node);
        }
    }

}
