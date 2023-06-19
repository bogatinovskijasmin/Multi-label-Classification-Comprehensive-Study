
package clus.ext.ensembles.induceCallables;

import java.util.concurrent.Callable;

import clus.data.rows.TupleIterator;
import clus.ext.ensembles.ClusEnsembleInduce;
import clus.ext.ensembles.containters.OneBagResults;
import clus.main.ClusRun;
import clus.main.ClusStatManager;
import clus.selection.BaggingSelection;
import clus.selection.OOBSelection;
import clus.util.ClusRandomNonstatic;


public class InduceOneBagCallable implements Callable<OneBagResults> {

    private ClusEnsembleInduce m_Cei;
    private ClusRun m_Cr;
    private int m_I, m_OrigMaxDepth;
    private OOBSelection m_Oob_sel, m_Oob_total;
    private TupleIterator m_Train_iterator, m_Test_iterator;
    private BaggingSelection m_Msel;
    private ClusRandomNonstatic m_Rnd;
    private ClusStatManager m_Mgr;


    public InduceOneBagCallable(ClusEnsembleInduce cei, ClusRun cr, int i, int origMaxDepth, OOBSelection oob_sel, OOBSelection oob_total, TupleIterator train_iterator, TupleIterator test_iterator, BaggingSelection msel, ClusRandomNonstatic rnd, ClusStatManager mgr) {
        this.m_Cei = cei;
        this.m_Cr = cr;
        this.m_I = i;
        this.m_OrigMaxDepth = origMaxDepth;
        this.m_Oob_sel = oob_sel;
        this.m_Oob_total = oob_total;
        this.m_Train_iterator = train_iterator;
        this.m_Test_iterator = test_iterator;
        this.m_Msel = msel;
        this.m_Rnd = rnd;
        this.m_Mgr = mgr;
    }


    @Override
    public OneBagResults call() throws Exception {
        return m_Cei.induceOneBag(m_Cr, m_I, m_OrigMaxDepth, m_Oob_sel, m_Oob_total, m_Train_iterator, m_Test_iterator, m_Msel, m_Rnd, m_Mgr);
    }

}
