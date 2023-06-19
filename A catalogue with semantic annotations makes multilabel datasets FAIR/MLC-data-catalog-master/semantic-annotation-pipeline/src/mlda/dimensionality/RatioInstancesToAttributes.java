/*
 * This file is part of the MLDA.
 *
 * (c)  Jose Maria Moyano Murillo
 *      Eva Lucrecia Gibaja Galindo
 *      Sebastian Ventura Soto <sventura@uco.es>
 *
 * For the full copyright and license information, please view the LICENSE
 * file that was distributed with this source code.
 */

package mlda.dimensionality;

import mlda.base.MLDataMetric;
import mulan.data.MultiLabelInstances;

/**
* Class implementing the Ratio of number of instances to the number of attributes
*
* @author Jose Maria Moyano Murillo
*/
public class RatioInstancesToAttributes extends MLDataMetric {

	/**
	 * Constructor
	 */
	public RatioInstancesToAttributes() {
		super("Ratio of number of instances to the number of attributes");
	}
	
	/**
	 * Calculate metric value
	 * 
	 * @param mlData Multi-label dataset to which calculate the metric
	 * @return Value of the metric
	 */
	public double calculate(MultiLabelInstances mlData){
		this.value = ((double)mlData.getNumInstances()) / mlData.getFeatureIndices().length;
		return value;
	}

}
