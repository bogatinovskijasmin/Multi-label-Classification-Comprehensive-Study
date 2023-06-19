package mulan.data.characterizer;

import mulan.data.LabelSet;
import mulan.data.MultiLabelInstances;
import mulan.dimensionalityReduction.BinaryRelevanceAttributeEvaluator;
import weka.attributeSelection.ASEvaluation;
import weka.attributeSelection.InfoGainAttributeEval;
import weka.core.*;

import java.util.*;

/**
 * Created by IntelliJ IDEA.
 * User: lenat
 * Date: 22/02/2011
 */
public class StatisticalCharacteristics {

    private static int binaryAtts = 0;

    public static void reset() {
        StatisticalCharacteristics.binaryAtts = 0;
    }

    public static class AverageGainRatio extends Characteristic {
        @Override
        public double compute(MultiLabelInstances train, MultiLabelInstances test) {
            try {
                Instances instances = train.getDataSet();
                double res = 0.0;
                ASEvaluation ase = new InfoGainAttributeEval();
                BinaryRelevanceAttributeEvaluator eval = new BinaryRelevanceAttributeEvaluator(ase, train, "avg", "none", "eval");
                int[] ints = train.getFeatureIndices();
                for (int i : ints) {
                    double v = eval.evaluateAttribute(i);
                    res += v;
                }
                value = res / ints.length;
            }
            catch (Exception e) {
                value = Double.NaN;
                e.printStackTrace();
            }
            return value;
        }
    }

    public static class ProportionWithOutliers extends Characteristic {
        @Override
        public double compute(MultiLabelInstances train, MultiLabelInstances test) {
            Instances instances = train.getDataSet();
            int num = instances.size();
            double alpha = 0.05;
            int numToTrimAtSide = (int) (num * alpha / 2);
            int countNumeric = 0;
            int countWithOutliers = 0;
            int[] ints = train.getFeatureIndices();
            for (int i : ints) {
                Attribute att = instances.attribute(i);
                if (att.isNumeric()) {
                    countNumeric++;
                    double variance = instances.variance(att);
                    double[] values = instances.attributeToDoubleArray(i);
                    Arrays.sort(values);
                    double[] trimmed = new double[num - (numToTrimAtSide * 2)];
                    for (int j = 0; j < trimmed.length; j++) {
                        trimmed[j] = values[j + numToTrimAtSide];
                    }
                    double varianceTrimmed = Utils.variance(trimmed);
                    double ratio = varianceTrimmed / variance;
                    if (ratio < 0.7) {
                        countWithOutliers++;
                    }
                }
            }
            if (countNumeric > 0) {
                value = (double) countWithOutliers / countNumeric;
            } else {
                //no numeric attributes in dataset
                value = Double.NaN;
            }
            return value;
        }
    }

    public static class AverageAbsoluteCorrelation extends Characteristic {
        @Override
        public double compute(MultiLabelInstances train, MultiLabelInstances test) {
            Instances instances = train.getDataSet();
            int num = instances.size();
            double res = 0.0;
            int count = 0;
            int[] featureIndices = train.getFeatureIndices();
            for (int ind1 : featureIndices) {
                if (instances.attribute(ind1).isNumeric()) {
                    for (int ind2 = ind1 + 1; ind2 < featureIndices.length; ind2++) {
                        if (instances.attribute(ind2).isNumeric()) {
                            count++;
                            double[] attVals1 = instances.attributeToDoubleArray(ind1);
                            double[] attVals2 = instances.attributeToDoubleArray(ind2);
                            res += Utils.correlation(attVals1, attVals2, num);
                        }
                    }
                }
            }
            if (count > 0) {
                value = res / count;
            } else {
                //no numeric attributes in dataset
                value = Double.NaN;
            }
            return value;
        }
    }

    public static class MeanOfEntropies extends Characteristic {
        @Override
        public double compute(MultiLabelInstances train, MultiLabelInstances test) {
            Instances instances = train.getDataSet();
            double res = 0.0;
            int countNominal = 0;
            int[] featureIndices = train.getFeatureIndices();
            for (int ind : featureIndices) {
                AttributeStats stats = instances.attributeStats(ind);
                if (stats.nominalCounts != null) {
                    countNominal++;
                    res += entropy(stats.nominalCounts);
                }
            }
            value = res / countNominal;
            return value;
        }
    }


    public static class MeanKurtosis extends Characteristic {
        @Override
        public double compute(MultiLabelInstances train, MultiLabelInstances test) {
            Instances instances = train.getDataSet();
            int num = instances.size();
            double res = 0.0;
            double avg;
            double var2;
            double var4;
            double val;
            int countNumeric = 0;
            int[] ints = train.getFeatureIndices();
            for (int i : ints) {
                Attribute att = instances.attribute(i);
                if (att.isNumeric()) {
                    countNumeric++;
                    avg = instances.meanOrMode(att);
                    var2 = 0;
                    var4 = 0;
                    for (Instance instance : instances) {
                        val = instance.value(att);
                        var4 += Math.pow(val - avg, 4);
                        var2 += Math.pow(val - avg, 2);
                    }
                    double kurtosis = (num*var4/Math.pow(var2,2))-3;
                    double  sampleKurtosis = (kurtosis*(num+1) + 6) * (num-1)/((num-2)*(num-3));
                    res += sampleKurtosis;
                }
            }
            if (countNumeric > 0) {
                value = res / countNumeric;
            } else {
                //no numeric attributes in dataset
                value = Double.NaN;
            }
            return value;
        }
    }

    public static class MeanSkewness extends Characteristic {
        @Override
        public double compute(MultiLabelInstances train, MultiLabelInstances test) {
            Instances instances = train.getDataSet();
            int num = instances.size();
            double res = 0.0;
            double stdev;
            double avg;
            double var;
            double val;
            int countNumeric = 0;
            int[] ints = train.getFeatureIndices();
            for (int i : ints) {
                Attribute att = instances.attribute(i);
                if (att.isNumeric()) {
                    countNumeric++;
                    avg = instances.meanOrMode(att);
                    var = 0;
                    for (Instance instance : instances) {
                        val = instance.value(att);
                        var += Math.pow(val - avg, 3);
                    }
                    double variance = instances.variance(att);
                    stdev = Math.sqrt(variance);
                    double skewness = num*var / ((num - 1) *(num-2)* Math.pow(stdev, 3));
                    res += skewness;
                }
            }
            if (countNumeric > 0) {
                value = res / countNumeric;
            } else {
                //no numeric attributes in dataset
                value = Double.NaN;
            }
            return value;
        }
    }

    public static class MeanOfStDev extends Characteristic {
        @Override
        public double compute(MultiLabelInstances train, MultiLabelInstances test) {
            Instances instances = train.getDataSet();
            double res = 0.0;
            double dev;
            int countNumeric = 0;
            int[] ints = train.getFeatureIndices();
            for (int i : ints) {
                Attribute att = instances.attribute(i);
                if (att.isNumeric()) {
                    countNumeric++;
                    double variance = instances.variance(att);
                    dev = Math.sqrt(variance);
                    res += dev;
                }
            }
            if (countNumeric > 0) {
                value = res / countNumeric;
            } else {
                //no numeric attributes in dataset
                value = Double.NaN;
            }
            return value;
        }
    }

    public static class MeanOfMeans extends Characteristic {
        @Override
        public double compute(MultiLabelInstances train, MultiLabelInstances test) {
            Instances instances = train.getDataSet();
            double res = 0.0;
            int countNumeric = 0;
            Set<Attribute> attributeSet = train.getFeatureAttributes();
            for (Attribute att : attributeSet) {
                if (att.isNumeric()) {
                    countNumeric++;
                    res += instances.meanOrMode(att);
                }
            }
            value = res / countNumeric;
            return value;
        }
    }

    public static class DefaultAccuracy extends Characteristic {
        @Override
        public double compute(MultiLabelInstances train, MultiLabelInstances test) {
            try {
                int total = train.getNumInstances();
                mulan.data.Statistics st =  new mulan.data.Statistics();
                st.calculateStats(train);
                HashMap<LabelSet, Integer> map = st.labelCombCount();
                Collection<Integer> values = map.values();
                SortedSet<Integer> sorted = new TreeSet<Integer>(values);
                double res = sorted.last();
                value = res / total;
            } catch (Exception e) {
                value = 0;
                e.printStackTrace();
            }
            return value;
        }
    }

    public static class CategoricalAttsRatio extends Characteristic {
        @Override
        public double compute(MultiLabelInstances train, MultiLabelInstances test) {
            int res = 0;
            Set<Attribute> attributeSet = train.getFeatureAttributes();
            int total = attributeSet.size();
            for (Attribute att : attributeSet) {
                if (att.isNominal()) {
                    res++;
                }
            }
            value = (double) res / total;
            return value;
        }
    }

    public static class BinaryAttsRatio extends Characteristic {
        @Override
        public double compute(MultiLabelInstances train, MultiLabelInstances test) {
            Set<Attribute> attributeSet = train.getFeatureAttributes();
            int total = attributeSet.size();
            value = (double) binaryAtts / total;
            return value;
        }
    }

    public static class NumOfBinaryAtts extends Characteristic {
        @Override
        public double compute(MultiLabelInstances train, MultiLabelInstances test) {
            int res = 0;
            Set<Attribute> attributeSet = train.getFeatureAttributes();
            for (Attribute att : attributeSet) {
                if (att.isNominal()) {
                    int numOfElements = 0;
                    Enumeration enumeration = att.enumerateValues();
                    while (enumeration.hasMoreElements()) {
                        enumeration.nextElement();
                        numOfElements++;
                    }
                    if (numOfElements == 2) res++;
                }
            }
            binaryAtts = res;
            value = res;
            return value;
        }

        @Override
        public String getCSVformat() {
            return "%.0f";
        }
    }

    public static class TestToAttsRatio extends Characteristic {
        @Override
        public double compute(MultiLabelInstances train, MultiLabelInstances test) {
            int numOfTest = test.getNumInstances();
            int att = train.getFeatureAttributes().size();
            if (att == 0) value = Double.NaN;
            else value = (double) numOfTest/att;
            return value;
        }
    }

    public static class TrainToAttsRatio extends Characteristic {
        @Override
        public double compute(MultiLabelInstances train, MultiLabelInstances test) {
            int numOfTrain = train.getNumInstances();
            int att = train.getFeatureAttributes().size();
            if (att == 0) value = Double.NaN;
            else value = (double) numOfTrain/att;
            return value;
        }
    }

    public static class NumOfAttributes extends Characteristic {
        @Override
        public double compute(MultiLabelInstances train, MultiLabelInstances test) {
            value = train.getFeatureAttributes().size();
            return value;
        }

        @Override
        public String getCSVformat() {
            return "%.0f";
        }
    }

    public static class TrainTestRatio extends Characteristic {
        @Override
        public double compute(MultiLabelInstances train, MultiLabelInstances test) {
            value = (double) train.getNumInstances() / test.getNumInstances();
            return value;
        }
    }

    public static class NumOfTotal extends Characteristic {
        @Override
        public double compute(MultiLabelInstances train, MultiLabelInstances test) {
            value = train.getNumInstances() + test.getNumInstances();
            return value;
        }

        @Override
        public String getCSVformat() {
            return "%.0f";
        }
    }


    public static class NumOfTest extends Characteristic {
        @Override
        public double compute(MultiLabelInstances train, MultiLabelInstances test) {
            value = test.getNumInstances();
            return value;
        }

        @Override
        public String getCSVformat() {
            return "%.0f";
        }
    }

    public static class NumOfTrain extends Characteristic {
        @Override
        public double compute(MultiLabelInstances train, MultiLabelInstances test) {
            value = train.getNumInstances();
            return value;
        }

        @Override
        public String getCSVformat() {
            return "%.0f";
        }
    }

    //a code from Weka's InfoGainAttributeEval class count method was used as reference implementation for single-label data.
    public double[][][] buildAttsEvalMatrix(Instances data) {

        // int classIndex = data.classIndex();
        int numInstances = data.numInstances();
        int classIndex = data.numAttributes() - 1;
        int numClasses = data.attribute(classIndex).numValues();

        // Reserve space and initialize counters
        double[][][] counts = new double[data.numAttributes()][][];
        for (int k = 0; k < data.numAttributes(); k++) {
            if (k != classIndex) {
                int numValues = data.attribute(k).numValues();
                counts[k] = new double[numValues + 1][numClasses + 1];
            }
        }

        // Initialize counters
        double[] temp = new double[numClasses + 1];
        for (int k = 0; k < numInstances; k++) {
            Instance inst = data.instance(k);
            if (inst.classIsMissing()) {
                temp[numClasses] += inst.weight();
            } else {
                temp[(int) inst.classValue()] += inst.weight();
            }
        }
        for (int k = 0; k < counts.length; k++) {
            if (k != classIndex) {
                for (int i = 0; i < temp.length; i++) {
                    counts[k][0][i] = temp[i];
                }
            }
        }

        // Get counts
        for (int k = 0; k < numInstances; k++) {
            Instance inst = data.instance(k);
            for (int i = 0; i < inst.numValues(); i++) {
                if (inst.index(i) != classIndex) {
                    if (inst.isMissingSparse(i) || inst.classIsMissing()) {
                        if (!inst.isMissingSparse(i)) {
                            counts[inst.index(i)][(int) inst.valueSparse(i)][numClasses] +=
                                    inst.weight();
                            counts[inst.index(i)][0][numClasses] -= inst.weight();
                        } else if (!inst.classIsMissing()) {
                            counts[inst.index(i)][data.attribute(inst.index(i)).numValues()]
                                    [(int) inst.classValue()] += inst.weight();
                            counts[inst.index(i)][0][(int) inst.classValue()] -=
                                    inst.weight();
                        } else {
                            counts[inst.index(i)][data.attribute(inst.index(i)).numValues()]
                                    [numClasses] += inst.weight();
                            counts[inst.index(i)][0][numClasses] -= inst.weight();
                        }
                    } else {
                        counts[inst.index(i)][(int) inst.valueSparse(i)]
                                [(int) inst.classValue()] += inst.weight();
                        counts[inst.index(i)][0][(int) inst.classValue()] -= inst.weight();
                    }
                }
            }
        }
        return counts;
    }

    public static double entropy(int[] array) {
        double returnValue = 0, sum = 0;
        for (int i = 0; i < array.length; i++) {
            returnValue -= lnFunc(array[i]);
            sum += array[i];
        }
        if (Utils.eq(sum, 0)) {
            return 0;
        } else {
            return (returnValue + lnFunc(sum)) / (sum * Math.log(array.length));
        }
    }

    /**
     * Help method for computing entropy.
     */
    private static double lnFunc(double num) {

        // Constant hard coded for efficiency reasons
        if (num < 1e-6) {
            return 0;
        } else {
            return num * Math.log(num);
        }
    }

}