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

package mlda.attributes;

import mlda.base.MLDataMetric;
import mulan.data.MultiLabelInstances;
import mulan.dimensionalityReduction.BinaryRelevanceAttributeEvaluator;
import weka.attributeSelection.ASEvaluation;
import weka.attributeSelection.InfoGainAttributeEval;

/**
* Class implementing the Average gain ratio
*
* @author Jose Maria Moyano Murillo
*/
public class AvgGainRatio extends MLDataMetric{

	/**
	 * Constructor
	 */
	public AvgGainRatio() {
		super("Average gain ratio");
	}
	
	/**
	 * Calculate metric value
	 * 
	 * @param mlData Multi-label dataset to which calculate the metric
	 * @return Value of the metric
	 */
	public double calculate(MultiLabelInstances mlData){
		double res = 0.0;
        
        try{
            ASEvaluation ase = new InfoGainAttributeEval();
        
            BinaryRelevanceAttributeEvaluator eval = new BinaryRelevanceAttributeEvaluator(ase, mlData, "avg", "none", "eval");

            int [] featureIndices = mlData.getFeatureIndices();

            for(int i : featureIndices){
                res += eval.evaluateAttribute(i);
            }

            res = res / featureIndices.length;
        }
        catch(Exception e){
            e.printStackTrace();
        	res = Double.NaN;
        }
		
		this.value = res;
		return value;
	}

}
