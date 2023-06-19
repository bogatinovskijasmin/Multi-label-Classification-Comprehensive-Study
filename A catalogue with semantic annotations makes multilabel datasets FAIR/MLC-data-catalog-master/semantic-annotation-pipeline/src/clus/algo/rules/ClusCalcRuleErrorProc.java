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

/*
 * Created on Jun 27, 2005
 */

package clus.algo.rules;

import java.io.IOException;

import clus.data.rows.DataTuple;
import clus.error.ClusErrorList;
import clus.model.ClusModel;
import clus.model.processor.ClusModelProcessor;


public class ClusCalcRuleErrorProc extends ClusModelProcessor {

    protected int m_Subset;
    protected ClusErrorList m_Global;


    public ClusCalcRuleErrorProc(int subset, ClusErrorList global) {
        m_Subset = subset;
        m_Global = global;
    }


    public void modelUpdate(DataTuple tuple, ClusModel model) throws IOException {
        ClusRule rule = (ClusRule) model;
        ClusErrorList error = rule.getError(m_Subset);
        error.addExample(tuple, rule.getTargetStat());
    }


    public void terminate(ClusModel model) throws IOException {
        ClusRuleSet set = (ClusRuleSet) model;
        for (int i = 0; i < set.getModelSize(); i++) {
            ClusRule rule = set.getRule(i);
            rule.getError(m_Subset).updateFromGlobalMeasure(m_Global);
        }
    }


    public boolean needsModelUpdate() {
        return true;
    }
}
