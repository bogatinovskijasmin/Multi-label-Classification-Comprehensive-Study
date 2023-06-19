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

package clus.error.mlc;

import java.io.PrintWriter;

import clus.data.rows.DataTuple;
import clus.data.type.NominalAttrType;
import clus.error.ClusError;
import clus.error.ClusErrorList;
import clus.error.ClusNominalError;
import clus.main.Settings;
import clus.statistic.ClusStatistic;
import clus.util.ClusFormat;


/**
 * @author matejp
 * 
 *         Hamming loss is used in multi-label classification scenario.
 */
public class HammingLoss extends ClusNominalError {

    public final static long serialVersionUID = Settings.SERIAL_VERSION_ID;

    protected int m_NbWrong;// sum of |prediction(sample_i) SYMMETRIC DIFFERENCE target(sample_i)|, where prediction
                            // (target) of a sample_i is the predicted (true) label set.
    protected int m_NbKnown;// number of the examples seen


    public HammingLoss(ClusErrorList par, NominalAttrType[] nom) {
        super(par, nom);
        m_NbWrong = 0;
        m_NbKnown = 0;
    }


    public boolean shouldBeLow() {
        return true;
    }


    public void reset() {
        m_NbWrong = 0;
        m_NbKnown = 0;
    }


    public void add(ClusError other) {
        HammingLoss ham = (HammingLoss) other;
        m_NbWrong += ham.m_NbWrong;
        m_NbKnown += ham.m_NbKnown;
    }


    // NEDOTAKNJENO
    public void showSummaryError(PrintWriter out, boolean detail) {
        showModelError(out, detail ? 1 : 0);
    }
    // // A MA TO SPLOH SMISU?
    // public double getHammingLoss(int i) {
    // return getModelErrorComponent(i);
    // }


    public double getModelError() {
        return ((double) m_NbWrong) / m_Dim / m_NbKnown;
    }


    public void showModelError(PrintWriter out, int detail) {
        out.println(ClusFormat.FOUR_AFTER_DOT.format(getModelError()));
    }


    public String getName() {
        return "HammingLoss";
    }


    public ClusError getErrorClone(ClusErrorList par) {
        return new HammingLoss(par, m_Attrs);
    }


    public void addExample(DataTuple tuple, ClusStatistic pred) {
        int[] predicted = pred.getNominalPred();
        NominalAttrType attr;
        boolean atLeastOneKnown = false;
        for (int i = 0; i < m_Dim; i++) {
            attr = getAttr(i);
            if (!attr.isMissing(tuple)) {
                atLeastOneKnown = true;
                if (attr.getNominal(tuple) != predicted[i]) {
                    m_NbWrong++;
                }
            }
        }
        if (atLeastOneKnown) {
            m_NbKnown++;
        }
    }


    public void addExample(DataTuple tuple, DataTuple pred) {
        boolean atLeastOneKnown = false;
        NominalAttrType attr;
        for (int i = 0; i < m_Dim; i++) {
            attr = getAttr(i);
            if (!attr.isMissing(tuple)) {
                atLeastOneKnown = true;
                if (attr.getNominal(tuple) != attr.getNominal(pred)) {
                    m_NbWrong++;
                }
            }
        }
        if (atLeastOneKnown) {
            m_NbKnown++;
        }
    }


    // NEDOTAKNJENO
    public void addInvalid(DataTuple tuple) {
    }

}
