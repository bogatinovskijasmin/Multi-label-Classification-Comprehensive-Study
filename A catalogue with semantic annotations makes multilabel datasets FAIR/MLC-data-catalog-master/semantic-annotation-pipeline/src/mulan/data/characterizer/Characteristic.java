/*
 *    This program is free software; you can redistribute it and/or modify
 *    it under the terms of the GNU General Public License as published by
 *    the Free Software Foundation; either version 2 of the License, or
 *    (at your option) any later version.
 *
 *    This program is distributed in the hope that it will be useful,
 *    but WITHOUT ANY WARRANTY; without even the implied warranty of
 *    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 *    GNU General Public License for more details.
 *
 *    You should have received a copy of the GNU General Public License
 *    along with this program; if not, write to the Free Software
 *    Foundation, Inc., 675 Mass Ave, Cambridge, MA 02139, USA.
 */

/*
 *    Measure.java
 *    Copyright (C) 2009-2010 Aristotle University of Thessaloniki, Thessaloniki, Greece
 */
package mulan.data.characterizer;

import mulan.data.MultiLabelInstances;
import weka.core.SerializedObject;

/**
 * Interface for a data set characteristic.
 *
 */
public abstract class Characteristic {
    protected String name;
    protected double value;

    /**
     * Gets the name of a characteristic.
     * @return the name of a characteristic.
     */
    public String getName(){
        return this.getClass().getSimpleName();
    }

    /**
     * Gets the value of a characteristic.
     * @return the characteristic value computed on certain data set
     * @see mulan.data.characterizer.Characteristic#compute(mulan.data.MultiLabelInstances, mulan.data.MultiLabelInstances)
     */
    double getValue(){
        return value;
    }

    /**
     * Computes and sets the value of a characteristic for the given data set.
     *
     * @param train the train data set for which  characteristic has to be computed
     * @param test the test data set for which  characteristic has to be computed
     * @return 
     * @see mulan.data.characterizer.Characteristic#getValue()
     */
    public abstract double compute(MultiLabelInstances train, MultiLabelInstances test);

    public Characteristic makeCopy() throws Exception {
        return (Characteristic) new SerializedObject(this).getObject();
    }

    public String getCSVformat() {
        return "%.6f";
    }
}