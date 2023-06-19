
package clus.selection;

import clus.data.rows.DataTuple;
import clus.data.rows.RowData;
import clus.data.type.ClusAttrType;
import clus.data.type.ClusSchema;


public class CriterionBasedSelection {

    public static final boolean isMissing(DataTuple tuple, ClusAttrType[] attrs) {
        for (int i = 0; i < attrs.length; i++) {
            if (attrs[i].isMissing(tuple))
                return true;
        }
        return false;
    }


    public static final void clearMissingFlagTargetAttrs(ClusSchema schema) {
        ClusAttrType[] targets = schema.getAllAttrUse(ClusAttrType.ATTR_USE_TARGET);
        for (int i = 0; i < targets.length; i++) {
            targets[i].setNbMissing(0);
        }
    }


    public static final RowData removeMissingTarget(RowData data) {
        int nbrows = data.getNbRows();
        ClusAttrType[] targets = data.getSchema().getAllAttrUse(ClusAttrType.ATTR_USE_TARGET);
        BitMapSelection sel = new BitMapSelection(nbrows);
        for (int i = 0; i < nbrows; i++) {
            DataTuple tuple = data.getTuple(i);
            if (!isMissing(tuple, targets)) {
                sel.select(i);
            }
        }
        if (sel.getNbSelected() != nbrows) {
            System.out.println("Tuples with missing target: " + (nbrows - sel.getNbSelected()));
            return (RowData) data.selectFrom(sel, null); // no problem, parallelism comes later
        }
        else {
            return data;
        }
    }
}
