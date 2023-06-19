package mulan.data.characterizer;

import mulan.data.*;
import weka.core.AttributeStats;
import weka.core.Instances;
import weka.core.Utils;

import java.util.*;

/**
 * Created by IntelliJ IDEA.
 * User: lenat
 * Date: 22/02/2011
 */
public class MultilabelCharacteristics {

    private static double minOfLabelEntropies = 0;
    private static double maxOfLabelEntropies = 0;
    private static String[] trainClasses;
    private static String[] testClasses;
    private static int totalClasses = 0;
    private static int unseen = 0;
    private static int numLabels = 0;
    private static double power = 0;
    private static Statistics statsTrain =  new Statistics();
    private static Statistics statsTest =  new Statistics();
    private static double cardStdev = 0;
    private static int numDepPairs = 0;
    private static double ratioOfDepPairs = 0;
    private static double avgOfChiScores = 0;
    private static double ratioClassesWithUpTo2Examples = 0;
    private static double ratioClassesWithUpTo5Examples = 0;
    private static double ratioClassesWithUpTo10Examples = 0;
    private static double ratioClassesWithUpTo50Examples = 0;
    private static Integer[] combCounts;


    public static void reset() {
        MultilabelCharacteristics.minOfLabelEntropies = 0;
        MultilabelCharacteristics.maxOfLabelEntropies = 0;
        MultilabelCharacteristics.trainClasses = null;
        MultilabelCharacteristics.testClasses = null;
        MultilabelCharacteristics.totalClasses = 0;
        MultilabelCharacteristics.unseen = 0;
        MultilabelCharacteristics.numLabels = 0;
        MultilabelCharacteristics.power = 0;
        MultilabelCharacteristics.statsTrain = new Statistics();
        MultilabelCharacteristics.statsTest = new Statistics();
        MultilabelCharacteristics.cardStdev = 0;
        MultilabelCharacteristics.numDepPairs = 0;
        MultilabelCharacteristics.ratioOfDepPairs = 0;
        MultilabelCharacteristics.avgOfChiScores = 0;
        MultilabelCharacteristics.ratioClassesWithUpTo2Examples = 0;
        MultilabelCharacteristics. ratioClassesWithUpTo5Examples = 0;
        MultilabelCharacteristics. ratioClassesWithUpTo10Examples = 0;
        MultilabelCharacteristics.ratioClassesWithUpTo50Examples = 0;
        MultilabelCharacteristics.combCounts = null;
    }


    public static class AvgExamplesPerClass extends Characteristic {
        @Override
        public double compute(MultiLabelInstances train, MultiLabelInstances test) {
            int numExamples = train.getNumInstances();
            value = (double)numExamples/trainClasses.length;
            return value;
        }
    }


    public static class RatioClassesWithExamplesLessHalfAttributes extends Characteristic {
        @Override
        public double compute(MultiLabelInstances train, MultiLabelInstances test) {
            int numAtts = train.getFeatureAttributes().size();
            int num = numAtts / 2;
            int res = countUpTo(num);
            value = (double)res / combCounts.length;
            return value;
        }
    }

    public static class RatioClassesWithUpTo50Examples extends Characteristic {
        @Override
        public double compute(MultiLabelInstances train, MultiLabelInstances test) {
            value = ratioClassesWithUpTo50Examples;
            return value;
        }

    }

    public static class RatioClassesWithUpTo10Examples extends Characteristic {
        @Override
        public double compute(MultiLabelInstances train, MultiLabelInstances test) {
            value = ratioClassesWithUpTo10Examples;
            return value;
        }

    }

    public static class RatioClassesWithUpTo5Examples extends Characteristic {
        @Override
        public double compute(MultiLabelInstances train, MultiLabelInstances test) {
            value = ratioClassesWithUpTo5Examples;
            return value;
        }

    }


    public static class RatioClassesWithUpTo2Examples extends Characteristic {
        @Override
        public double compute(MultiLabelInstances train, MultiLabelInstances test) {
            value = ratioClassesWithUpTo2Examples;
            return value;
        }

    }

    public static class NumClassesWithUpTo50Examples extends Characteristic {
        @Override
        public double compute(MultiLabelInstances train, MultiLabelInstances test) {
            int res = countUpTo(50);
            value = res;
            ratioClassesWithUpTo50Examples = value / combCounts.length;
            return ratioClassesWithUpTo50Examples;
        }

        @Override
        public String getCSVformat() {
            return "%.0f";
        }
    }

    public static class NumClassesWithUpTo10Examples extends Characteristic {
        @Override
        public double compute(MultiLabelInstances train, MultiLabelInstances test) {
            int res = countUpTo(10);
            value = res;
            ratioClassesWithUpTo10Examples = value / combCounts.length;
            return ratioClassesWithUpTo10Examples;
        }

        @Override
        public String getCSVformat() {
            return "%.0f";
        }
    }


    public static class NumClassesWithUpTo5Examples extends Characteristic {
        @Override
        public double compute(MultiLabelInstances train, MultiLabelInstances test) {
            int res = countUpTo(5);
            value = res;
            ratioClassesWithUpTo5Examples = value / combCounts.length;
            return ratioClassesWithUpTo5Examples;
        }

        @Override
        public String getCSVformat() {
            return "%.0f";
        }
    }

    public static class NumClassesWithUpTo2Examples extends Characteristic {
        @Override
        public double compute(MultiLabelInstances train, MultiLabelInstances test) {
            Collection<Integer> counts = statsTrain.labelCombCount().values();
            combCounts = new Integer[counts.size()];
            counts.toArray(combCounts);
            Arrays.sort(combCounts);
            int res = countUpTo(2);
            value = res;
            ratioClassesWithUpTo2Examples = value / combCounts.length;
            return ratioClassesWithUpTo2Examples;
        }

        @Override
        public String getCSVformat() {
            return "%.0f";
        }
    }


    public static class AvgOfDepChiScores extends Characteristic {
        @Override
        public double compute(MultiLabelInstances train, MultiLabelInstances test) {
            //System.out.println("Calculating " + this.getName());
            value = avgOfChiScores;
            //System.out.println("Res= " + value);
            return value;
        }
    }

    public static class UncondDepPairsRatio extends Characteristic {
        @Override
        public double compute(MultiLabelInstances train, MultiLabelInstances test) {
            value = ratioOfDepPairs;
            return value;
        }
    }

    public static class UncondDepPairsNum extends Characteristic {
        @Override
        public double compute(MultiLabelInstances train, MultiLabelInstances test) {
            try {
                UnconditionalChiSquareIdentifier depid = new UnconditionalChiSquareIdentifier();
                LabelsPair[] pairs = depid.calculateDependence(train);
                int total = pairs.length;
                int dep=0;
                double sum= 0;
                double score=0;
                for (int i=0;i<total;i++){
                    score = pairs[i].getScore();
                    if(score > 6.635){
                        dep++;
                        sum+=score;
                    }
                    else{
                        break;
                    }
                }
                ratioOfDepPairs = (double)dep / total;
                avgOfChiScores = sum / dep;
                numDepPairs = dep;
                value = numDepPairs;
            } catch (Exception e) {
                value = 0;
                e.printStackTrace();
            }
            
            return value;
        }


        @Override
        public String getCSVformat() {
            return "%.0f";
        }
    }

    public static class LabelDensityTrain extends Characteristic {
        @Override
        public double  compute(MultiLabelInstances train, MultiLabelInstances test) {
            try {
                value = statsTrain.density();
            } catch (Exception e) {
                value = 0;
                e.printStackTrace();
            }
            return value;
        }
    }

    public static class KurtosisOfTrainCardinality extends Characteristic {
        @Override
        public double compute(MultiLabelInstances train, MultiLabelInstances test) {
            try {
                double avg = statsTrain.cardinality();
                double sum2 = 0;
                double sum4 = 0;
                int[] labelsForInstance = statsTrain.getNumLabelsForInstance();
                for (int i=0; i<labelsForInstance.length;i++) {
                    double v = labelsForInstance[i] - avg;
                    sum2 += Math.pow(v, 2);
                    sum4 += Math.pow(v, 4);
                }
                int num = labelsForInstance.length;
                double kurtosis = (num*sum4/Math.pow(sum2,2))-3;
                double  sampleKurtosis = (kurtosis*(num+1) + 6) * (num-1)/((num-2)*(num-3));
                value = sampleKurtosis;
            } catch (Exception e) {
                value = 0;
                e.printStackTrace();
            }
            return value;
        }
    }

    public static class SkewnessOfTrainCardinality extends Characteristic {
        @Override
        public double compute(MultiLabelInstances train, MultiLabelInstances test) {
            try {
                double avg = statsTrain.cardinality();
                double sum = 0;
                int[] labelsForInstance = statsTrain.getNumLabelsForInstance();
                for (int i=0; i<labelsForInstance.length;i++) {
                    double v = labelsForInstance[i] - avg;
                    sum += Math.pow(v, 3);
                }
                int num = labelsForInstance.length;
                double skewness = num * sum / ((num - 1)*(num-2) * Math.pow(cardStdev, 3));
                value = skewness;
            } catch (Exception e) {
                value = 0;
                e.printStackTrace();
            }
            return value;
        }
    }

    public static class StDevOfTrainCardinality extends Characteristic {
        @Override
        public double compute(MultiLabelInstances train, MultiLabelInstances test) {
            try {
                double avg = statsTrain.cardinality();
                double sum = 0;
                int[] labelsForInstance = statsTrain.getNumLabelsForInstance();
                for (int i=0; i<labelsForInstance.length;i++) {
                    double v = labelsForInstance[i] - avg;
                    sum += Math.pow(v, 2);
                }
                double var = sum / (labelsForInstance.length - 1);
                cardStdev  = Math.sqrt(var);
                value = cardStdev;
            } catch (Exception e) {
                value = 0;
                e.printStackTrace();
            }
            return value;
        }
    }

    public static class AbsDifferenceOfCardinality extends Characteristic {
        @Override
        public double compute(MultiLabelInstances train, MultiLabelInstances test) {
            try {
                double diff = statsTest.cardinality() - statsTrain.cardinality();
                value = Math.abs(diff);
            } catch (Exception e) {
                value = 0;
                e.printStackTrace();
            }
            return value;
        }
    }

    public static class LabelCardinalityTest extends Characteristic {
        @Override
        public double compute(MultiLabelInstances train, MultiLabelInstances test) {
            try {
                statsTest.calculateStats(test);
                value = statsTest.cardinality();
            } catch (Exception e) {
                value = 0;
                e.printStackTrace();
            }
            return value;
        }
    }

    public static class LabelCardinalityTrain extends Characteristic {
        @Override
        public double compute(MultiLabelInstances train, MultiLabelInstances test) {
            try {
                statsTrain.calculateStats(train);
                value = statsTrain.cardinality();
            } catch (Exception e) {
                value = 0;
                e.printStackTrace();
            }
            return value;
        }
    }

    public static class RatioUnseenToTest extends Characteristic {
        @Override
        public double compute(MultiLabelInstances train, MultiLabelInstances test) {
            try {
                value = (double)unseen / testClasses.length;
            } catch (Exception e) {
                value = 0;
                e.printStackTrace();
            }
            return value;
        }
    }


    public static class RatioTotalToPower extends Characteristic {
        @Override
        public double compute(MultiLabelInstances train, MultiLabelInstances test) {
            try {
                value = (double)totalClasses / power;
            } catch (Exception e) {
                value = 0;
                e.printStackTrace();
            }
            return value;
        }
    }


    public static class RatioTestToPower extends Characteristic {
        @Override
        public double compute(MultiLabelInstances train, MultiLabelInstances test) {
            try {
                value = (double)testClasses.length / power;
            } catch (Exception e) {
                value = 0;
                e.printStackTrace();
            }
            return value;
        }
    }

    public static class RatioTrainToPower extends Characteristic {
        @Override
        public double compute(MultiLabelInstances train, MultiLabelInstances test) {
            try {
                power = Math.pow(2,numLabels);
                value = (double)trainClasses.length / power;
            } catch (Exception e) {
                value = 0;
                e.printStackTrace();
            }
            return value;
        }
    }

    public static class UnseenInTrain extends Characteristic {
        @Override
        public double compute(MultiLabelInstances train, MultiLabelInstances test) {
            try {
                int count = 0;
                Collection tr = Arrays.asList(trainClasses);
                Collection ts = Arrays.asList(testClasses);
                for (Iterator iterator = ts.iterator(); iterator.hasNext();) {
                    String val =  (String)iterator.next();
                    if(!tr.contains(val)) count++;
                }
                unseen = count;
                value = unseen;
            } catch (Exception e) {
                value = 0;
                e.printStackTrace();
            }
            return value;
        }

        @Override
        public String getCSVformat() {
            return "%.0f";
        }
    }

    public static class TotalDistinctClasses extends Characteristic {
        @Override
        public double compute(MultiLabelInstances train, MultiLabelInstances test) {
            try {
                Collection coll1 = Arrays.asList(trainClasses);
                Collection coll2 = Arrays.asList(testClasses);
                SortedSet merged = new TreeSet(coll1);
                merged.addAll(coll2);
                totalClasses = merged.size();
                value = totalClasses;
            } catch (Exception e) {
                value = 0;
                e.printStackTrace();
            }
            return value;
        }

        @Override
        public String getCSVformat() {
            return "%.0f";
        }
    }

    public static class NumOfTestDistinctClasses extends Characteristic {
        @Override
        public double compute(MultiLabelInstances train, MultiLabelInstances test) {
            try {
                testClasses = getDistinctClasses(test);
                value = testClasses.length;
            } catch (Exception e) {
                value = 0;
                e.printStackTrace();
            }
            return value;
        }

        @Override
        public String getCSVformat() {
            return "%.0f";
        }
    }

    public static class NumOfTrainDistinctClasses extends Characteristic {
        @Override
        public double compute(MultiLabelInstances train, MultiLabelInstances test) {
            try {
                trainClasses = getDistinctClasses(train);
                value = trainClasses.length;
            } catch (Exception e) {
                value = 0;
                e.printStackTrace();
            }
            return value;
        }

        @Override
        public String getCSVformat() {
            return "%.0f";
        }
    }


    public static class NumberOfLabels extends Characteristic {
        @Override
        public double compute(MultiLabelInstances train, MultiLabelInstances test) {
            numLabels = train.getNumLabels();
            value = numLabels;
            return value;
        }
    }



    public static class MinOfLabelEntropies extends Characteristic {
        @Override
        public double  compute(MultiLabelInstances train, MultiLabelInstances test) {
            value = minOfLabelEntropies;
            return value;
        }
    }

    public static class MaxOfLabelEntropies extends Characteristic {
        @Override
        public double compute(MultiLabelInstances train, MultiLabelInstances test) {
            Instances instances = train.getDataSet();
            int[] labels = train.getLabelIndices();
            double[] vals = new double[labels.length];
            for (int i = 0; i < labels.length; i++) {
                AttributeStats stats = instances.attributeStats(labels[i]);
                if (stats.nominalCounts != null) {
                    vals[i] = entropy(stats.nominalCounts);
                }
            }
            Arrays.sort(vals);
            minOfLabelEntropies = vals[0];
            maxOfLabelEntropies = vals[labels.length-1];
            value = maxOfLabelEntropies;
            return value;
        }
    }


    public static class MeanOfLabelEntropies extends Characteristic {
        @Override
        public double compute(MultiLabelInstances train, MultiLabelInstances test) {
            Instances instances = train.getDataSet();
            double res = 0.0;
            int countNominal = 0;
            int[] labels = train.getLabelIndices();
            for (int i = 0; i < labels.length; i++) {
                AttributeStats stats = instances.attributeStats(labels[i]);
                if (stats.nominalCounts != null) {
                    countNominal++;
                    res += entropy(stats.nominalCounts);
                }
            }
            value = res / countNominal;
            return value;
        }

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


    public static String[] getDistinctClasses(MultiLabelInstances train) throws Exception {
        int total = train.getNumInstances();
        mulan.data.Statistics st =  new mulan.data.Statistics();
        st.calculateStats(train);
        Set<LabelSet> sets = st.labelSets();
        String[] classes = new String[sets.size()];
        Iterator<LabelSet> labelSetIterator = sets.iterator();
        for (int i=0;i<sets.size();i++) {
            LabelSet set = labelSetIterator.next();
            classes[i] = set.toBitString();
        }
        return classes;
    }

    protected static int countUpTo(int num) {
        int res=0;
        for (int i=0; i<combCounts.length; i++){
            if(combCounts[i]<=num){
                res++;
            }
            else{
                break;
            }
        }
        return res;
    }

}
