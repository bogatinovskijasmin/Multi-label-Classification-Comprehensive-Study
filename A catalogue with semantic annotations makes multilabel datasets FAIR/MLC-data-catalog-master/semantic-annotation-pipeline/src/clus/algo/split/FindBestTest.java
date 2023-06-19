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

package clus.algo.split;

import java.util.ArrayList;
import java.util.Random;

import clus.data.rows.DataTuple;
import clus.data.rows.RowData;
import clus.data.rows.RowDataSortHelper;
import clus.data.type.ClusSchema;
import clus.data.type.NominalAttrType;
import clus.data.type.NumericAttrType;
import clus.data.type.SparseNumericAttrType;
import clus.ext.ensembles.ClusEnsembleInduce;
import clus.heuristic.VarianceReductionHeuristicEfficient;
import clus.main.ClusStatManager;
import clus.main.Settings;
import clus.statistic.ClusStatistic;
import clus.util.ClusException;
import clus.util.ClusRandom;
import clus.util.ClusRandomNonstatic;


public class FindBestTest {

    public CurrentBestTestAndHeuristic m_BestTest = new CurrentBestTestAndHeuristic();
    // public long m_Timer = 0;
    protected RowDataSortHelper m_SortHelper = new RowDataSortHelper();

    protected ClusStatManager m_StatManager;
    protected NominalSplit m_Split;
    protected int m_MaxStats;
    

    public FindBestTest(ClusStatManager mgr) {
        m_StatManager = mgr;
        m_MaxStats = getSchema().getMaxNbStats();
    }


    public FindBestTest(ClusStatManager mgr, NominalSplit split) {
        m_StatManager = mgr;
        m_Split = split;
        m_MaxStats = getSchema().getMaxNbStats();
    }


    public ClusSchema getSchema() {
        return getStatManager().getSchema();
    }


    public ClusStatManager getStatManager() {
        return m_StatManager;
    }


    public RowDataSortHelper getSortHelper() {
        return m_SortHelper;
    }


    public Settings getSettings() {
        return getStatManager().getSettings();
    }


    public CurrentBestTestAndHeuristic getBestTest() {
        return m_BestTest;
    }


    public void cleanSplit() {
        m_Split = null;
    }


    public void findNominal(NominalAttrType at, RowData data, ClusRandomNonstatic rnd) {
        // Reset positive statistic
        // long start_time = System.currentTimeMillis();
        RowData sample = createSample(data, rnd);
        int nbvalues = at.getNbValues();
        m_BestTest.reset(nbvalues + 1);
        int nb_rows = sample.getNbRows();
        if (nbvalues == 2 && !at.hasMissing()) {
            // Only count ones for binary attributes (optimization)
            for (int i = 0; i < nb_rows; i++) {
                DataTuple tuple = sample.getTuple(i);
                int value = at.getNominal(tuple);
                // The value "1" has index 0 in the list of attribute values
                if (value == 0) {
                    m_BestTest.m_TestStat[0].updateWeighted(tuple, i);
                }
            }
            // Also compute the statistic for the zeros
            m_BestTest.m_TestStat[1].copy(m_BestTest.m_TotStat);
            m_BestTest.m_TestStat[1].subtractFromThis(m_BestTest.m_TestStat[0]);
        }
        else {
            // Regular code for non-binary attributes
            for (int i = 0; i < nb_rows; i++) {
                DataTuple tuple = sample.getTuple(i);
                int value = at.getNominal(tuple);
                m_BestTest.m_TestStat[value].updateWeighted(tuple, i);
            }
        }

        /*
         * long stop_time = System.currentTimeMillis();
         * long elapsed = stop_time - start_time;
         * m_Timer += elapsed;
         */

        // System.out.println("done");

        // Find best split
        m_Split.findSplit(m_BestTest, at);
    }


    // @Deprecated
    // public void findNominalRandom(NominalAttrType at, RowData data, ClusRandomNonstatic rnd) {
    // Random rn;
    // if(rnd == null){
    // rn = ClusRandom.getRandom(ClusRandom.RANDOM_EXTRATREE);
    // } else{
    // rn = rnd.getRandom(ClusRandomNonstatic.RANDOM_EXTRATREE);
    // }
    //
    // // Reset positive statistic
    // RowData sample = createSample(data, rnd);
    // int nbvalues = at.getNbValues();
    // m_BestTest.reset(nbvalues + 1);
    // // For each attribute value
    // int nb_rows = sample.getNbRows();
    // for (int i = 0; i < nb_rows; i++) {
    // DataTuple tuple = sample.getTuple(i);
    // int value = at.getNominal(tuple);
    // m_BestTest.m_TestStat[value].updateWeighted(tuple, i);
    // }
    // // Find the split
    // m_Split.findRandomSplit(m_BestTest, at, rn);
    // }

    public void findNominalExtraTree(NominalAttrType at, RowData data, ClusRandomNonstatic rnd) {
        Random rn;
        if (rnd == null) {
            rn = ClusRandom.getRandom(ClusRandom.RANDOM_EXTRATREE);
            ClusEnsembleInduce.giveParallelisationWarning(ClusEnsembleInduce.m_PARALLEL_TRAP_staticRandom);
        }
        else {
            rn = rnd.getRandom(ClusRandomNonstatic.RANDOM_EXTRATREE);
        }
        // Reset positive statistic
        RowData sample = createSample(data, rnd);
        int nbvalues = at.getNbValues();
        m_BestTest.reset(nbvalues + 1);
        // For each attribute value
        int nb_rows = sample.getNbRows();
        for (int i = 0; i < nb_rows; i++) {
            DataTuple tuple = sample.getTuple(i);
            int value = at.getNominal(tuple);
            m_BestTest.m_TestStat[value].updateWeighted(tuple, i);
        }
        // Find the split
        m_Split.findExtraTreeSplit(m_BestTest, at, rn);
    }


    public void findNumeric(NumericAttrType at, RowData data, ClusRandomNonstatic rnd) {
        RowData sample = createSample(data, rnd);
        DataTuple tuple;
//        if (at.isSparse()) {
//            sample.sortSparse(at, m_SortHelper);
//        }
//        else {
//            sample.sort(at);
//        }
        Integer[] indicesSorted = sample.smartSort(at);
        
        m_BestTest.reset(2);
        // Missing values
        int pos = 0;
        int nb_rows = sample.getNbRows();
        // Copy total statistic into corrected total
        m_BestTest.copyTotal();
        if (at.hasMissing()) {
            // Because of sorting, all missing values are in the front :-)
            while (pos < nb_rows && at.isMissing(tuple = sample.getTuple(indicesSorted[pos]))) {
                m_BestTest.m_MissingStat.updateWeighted(tuple, indicesSorted[pos]);
                pos++;
            }
            m_BestTest.subtractMissing();
        }
        double minValue =  (pos < nb_rows) ? at.getNumeric(sample.getTuple(indicesSorted[nb_rows - 1])) : Double.NaN;
        double prev = Double.NaN;
        boolean isSparseAtr = at.isSparse();
        
        double tot_corr_SVarS = 0.0;  // does not matter to which value we choose;
//        boolean isEfficient = m_BestTest.m_Heuristic.isEfficient();
//		if(isEfficient){
//			tot_corr_SVarS = m_BestTest.m_TotCorrStat.getSVarS(m_BestTest.m_Heuristic.getClusteringAttributeWeights());
////			m_BestTest.m_Heuristic.setSplitStatSVarS(tot_corr_SVarS);
//		}
        
        for (int i = pos; i < nb_rows; i++) {
            tuple = sample.getTuple(indicesSorted[i]);
            double value = at.getNumeric(tuple);
            if (value != prev) {
            	m_BestTest.updateNumeric(value, at, tot_corr_SVarS, false); // isEfficient
                prev = value;
            }
            m_BestTest.m_PosStat.updateWeighted(tuple, i);
            if (isSparseAtr && value == minValue){
            	break;
            }
        }
    }


    public void findNumericExtraTree(NumericAttrType at, RowData orig_data, ClusRandomNonstatic rnd) {
        // TODO: if this method gets completed, sampling of the RowDatas must be included as well

        Random rn;
        if (rnd == null) {
            rn = ClusRandom.getRandom(ClusRandom.RANDOM_EXTRATREE);
            ClusEnsembleInduce.giveParallelisationWarning(ClusEnsembleInduce.m_PARALLEL_TRAP_staticRandom);
        }
        else {
            rn = rnd.getRandom(ClusRandomNonstatic.RANDOM_EXTRATREE);
        }

        RowData data = createSample(orig_data, rnd);
        DataTuple tuple;
        int idx = at.getArrayIndex();

        // Sort values from large to small
        // if (at.isSparse()) {
        // data.sortSparse(at, m_SortHelper);
        // } else {
        // data.sort(at);
        // }

        Integer[] indicesSorted = data.smartSort(at);

        m_BestTest.reset(2);
        // Missing values
        int pos = 0;
        int nb_rows = data.getNbRows();
        // Copy total statistic into corrected total
        m_BestTest.copyTotal();
        if (at.hasMissing()) {
            // Because of sorting, all missing values are in the front :-)
            while (pos < nb_rows && (tuple = data.getTuple(indicesSorted[pos])).hasNumMissing(idx)) {
                m_BestTest.m_MissingStat.updateWeighted(tuple, indicesSorted[pos]);
                pos++;
            }
            m_BestTest.subtractMissing();
        }
        // now indicesSorted[pos] is the index of the tuple that has the highest (and non-missing) value of the attribute

        // Generate the random split value based on the original data
        if (pos == nb_rows) {// this can prevent illegal tests;
            m_BestTest.m_BestHeur = Double.NEGATIVE_INFINITY;
        }
        else {
            double min_value = data.getTuple(indicesSorted[nb_rows - 1]).getDoubleVal(idx);
            double max_value = data.getTuple(indicesSorted[pos]).getDoubleVal(idx);
            double split_value = (max_value - min_value) * rn.nextDouble() + min_value;
            for (int i = pos; i < nb_rows; i++) {
                tuple = data.getTuple(indicesSorted[i]);
                if (tuple.getDoubleVal(idx) <= split_value)
                    break;
                m_BestTest.m_PosStat.updateWeighted(tuple, indicesSorted[i]);
            }
            m_BestTest.updateNumeric(split_value, at);  // we test only one split per attribute --> no need for precomputing tot_corr_SVarS
        }

        // System.err.println("Inverse splits not yet included!");
        // TODO: m_Selector.updateInverseNumeric(split_value, at);
    }


   @Deprecated
    public void findNumeric(NumericAttrType at, ArrayList data){
    	 // for sparse attributes, (already sorted data)
        ArrayList sample;
        if (getSettings().getTreeSplitSampling() > 0) {
            RowData tmp = new RowData(data, getSchema());
            RowData smpl = createSample(tmp, null);
            if (at.isSparse()) {
                smpl.sortSparse(at, getSortHelper());
            }
            else {
                smpl.sort(at);
            }
            sample = smpl.toArrayList();
        }
        else {
            sample = data;
        }
        DataTuple tuple;
        m_BestTest.reset(2);
        // Missing values
        int first = 0;
        int nb_rows = sample.size();
        // Copy total statistic into corrected total
        m_BestTest.copyTotal();
        if (at.hasMissing()) {
            // Because of sorting, all missing values are in the front :-)
            while (first < nb_rows && at.isMissing((DataTuple) sample.get(first))) {
                tuple = (DataTuple) sample.get(first);
                m_BestTest.m_MissingStat.updateWeighted(tuple, first);
                first++;
            }
            m_BestTest.subtractMissing();
        }
        double prev = Double.NaN;

        for (int i = first; i < nb_rows; i++) {
            tuple = (DataTuple) sample.get(i);
            double value = at.getNumeric(tuple);
            if (value != prev) {
                if (!Double.isNaN(value)) {
                    // System.err.println("Value (>): " + value);
                    m_BestTest.updateNumeric(value, at);
                }
                prev = value;
            }
            m_BestTest.m_PosStat.updateWeighted(tuple, i);
        }
        m_BestTest.updateNumeric(0.0, at); // otherwise tests of the form "X>0.0" are not considered
    }

    @Deprecated
    public void findNumericRandom(NumericAttrType at, RowData data, RowData orig_data, Random rn) {
        // TODO: if this method gets completed, sampling of the RowDatas must be included as well
        DataTuple tuple;
        int idx = at.getArrayIndex();
        // Sort values from large to small
        if (at.isSparse()) {
            data.sortSparse(at, m_SortHelper);
        }
        else {
            data.sort(at);
        }
        m_BestTest.reset(2);
        // Missing values
        int first = 0;
        int nb_rows = data.getNbRows();
        // Copy total statistic into corrected total
        m_BestTest.copyTotal();
        if (at.hasMissing()) {
            // Because of sorting, all missing values are in the front :-)
            while (first < nb_rows && (tuple = data.getTuple(first)).hasNumMissing(idx)) {
                m_BestTest.m_MissingStat.updateWeighted(tuple, first);
                first++;
            }
            m_BestTest.subtractMissing();
        }
        // Do the same for original data, except updating the statistics:
        // Sort values from large to small
        if (at.isSparse()) {
            orig_data.sortSparse(at, m_SortHelper);
        }
        else {
            orig_data.sort(at);
        }
        // Missing values
        int orig_first = 0;
        int orig_nb_rows = orig_data.getNbRows();
        if (at.hasMissing()) {
            // Because of sorting, all missing values are in the front :-)
            while (orig_first < orig_nb_rows && (tuple = orig_data.getTuple(orig_first)).hasNumMissing(idx)) {
                orig_first++;
            }
        }
        // Generate the random split value based on the original data
        double min_value = orig_data.getTuple(orig_nb_rows - 1).getDoubleVal(idx);
        double max_value = orig_data.getTuple(orig_first).getDoubleVal(idx);
        double split_value = (max_value - min_value) * rn.nextDouble() + min_value;
        for (int i = first; i < nb_rows; i++) {
            tuple = data.getTuple(i);
            if (tuple.getDoubleVal(idx) <= split_value)
                break;
            m_BestTest.m_PosStat.updateWeighted(tuple, i);
        }
        m_BestTest.updateNumeric(split_value, at);
        System.err.println("Inverse splits not yet included!");
        // TODO: m_Selector.updateInverseNumeric(split_value, at);
    }


    public void initSelectorAndSplit(ClusStatistic totstat) throws ClusException {
        m_BestTest.create(m_StatManager, m_MaxStats);
        m_BestTest.setRootStatistic(totstat);
        if (getSettings().isBinarySplit())
            m_Split = new SubsetSplit();
        else
            m_Split = new NArySplit();
        m_Split.initialize(m_StatManager);
    }


    public boolean initSelectorAndStopCrit(ClusStatistic total, RowData data) {
        m_BestTest.initTestSelector(total, data);
        m_Split.setSDataSize(data.getNbRows());
        return m_BestTest.stopCrit();
    }


    public void setInitialData(ClusStatistic total, RowData data) throws ClusException {
        m_BestTest.setInitialData(total, data);
    }


    private RowData createSample(RowData original, ClusRandomNonstatic rnd) {
    	int N = getSettings().getTreeSplitSampling();
    	if (N == 0){
    		return original.sample(N, rnd);
    	}
    	else{
    		String message = String.format("The value of SplitSampling = %d will result in wrong results.\n"
    				+ "Use SplitSampling = 0 or correct the code.", N);
    		throw new RuntimeException(message);
    	}
    }

}
