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

package mlda.metricsTaxonomy;

import java.util.Arrays;

/**
* Class storing the dimensionality metrics names
*
* @author Jose Maria Moyano Murillo
*/
public class DimensionalityMetrics {
	
static String [] metrics = null;
	
	/**
	 * Get the names of the available attributes metrics
	 * 
	 * @return An array with the names
	 */
	public static String[] getAvailableMetrics(){
		if(metrics == null){
			defaultMetrics();
		}
		
		return metrics;
	}
	
	/**
	 * Add a metric to the list
	 * 
	 * @param newMetric Name of the metric to add
	 */
	public static void addMetric(String newMetric){
		if(metrics == null){
			defaultMetrics();
		}
		
		metrics = Arrays.copyOf(metrics, metrics.length+1);
		metrics[metrics.length - 1] = newMetric;
	}
	
	/**
	 * Fill the array with the default metrics
	 */
	private static void defaultMetrics(){
		String [] metrics = new String[6];
		
		metrics[0] = "Attributes";
		metrics[1] = "Instances";
		metrics[2] = "Labels";
		metrics[3] = "Distinct labelsets";
		metrics[4] = "LxIxF";
		metrics[5] = "Ratio of number of instances to the number of attributes";
	}

}
