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

package mlda.imbalance;

import mulan.data.MultiLabelInstances;

/**
* Class implementing the Mean of standard deviation of IR intra class
*
* @author Jose Maria Moyano Murillo
*/
public class MeanStdvIRIntraClass extends ImbalanceDataMetric{

	/**
	 * Constructor
	 */
	public MeanStdvIRIntraClass() {
		super("Mean of standard deviation of IR intra class");
	}
	
	/**
	 * Calculate metric value
	 * 
	 * @param mlData Multi-label dataset to which calculate the metric
	 * @return Value of the metric
	 */
	public double calculate(MultiLabelInstances mlData){
		super.calculate(mlData);
		
		double stdv = 0;
        
        for(int i=0; i<imbalancedData.length; i++){
        	stdv += Math.sqrt(imbalancedData[i].getVariance());
        }

		this.value = stdv/imbalancedData.length;
		return value;
	}

}
