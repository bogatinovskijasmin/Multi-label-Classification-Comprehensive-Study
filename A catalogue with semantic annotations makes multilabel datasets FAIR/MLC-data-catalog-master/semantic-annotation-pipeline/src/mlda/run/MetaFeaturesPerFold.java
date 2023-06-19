package mlda.run;

import java.io.File;
import java.io.FileNotFoundException;
import java.io.FileWriter;
import java.io.IOException;
import java.io.PrintWriter;
import java.util.ArrayList;

import org.json.simple.JSONArray;
import org.json.simple.JSONObject;

import mlda.attributes.AvgAbsoluteCorrelationBetweenNumericAttributes;
import mlda.attributes.AvgGainRatio;
import mlda.attributes.BinaryAttributes;
import mlda.attributes.MeanEntropiesNominalAttributes;
import mlda.attributes.MeanOfMeanOfNumericAttributes;
import mlda.attributes.MeanSkewnessNumericAttributes;
import mlda.attributes.MeanStdvNumericAttributes;
import mlda.attributes.NominalAttributes;
import mlda.attributes.NumericAttributes;
import mlda.attributes.ProportionBinaryAttributes;
import mlda.attributes.ProportionNominalAttributes;
import mlda.attributes.ProportionNumericAttributes;
import mlda.attributes.ProportionNumericAttributesWithOutliers;
import mlda.base.MLDataCharacterization;
import mlda.base.MLDataMetric;
import mlda.dimensionality.Attributes;
import mlda.dimensionality.DistinctLabelsets;
import mlda.dimensionality.Instances;
import mlda.dimensionality.Labels;
import mlda.dimensionality.LxIxF;
import mlda.dimensionality.RatioInstancesToAttributes;
import mlda.imbalance.CVIRInterClass;
import mlda.imbalance.ImbalanceDataMetric;
import mlda.imbalance.KurtosisCardinality;
import mlda.imbalance.MaxIRInterClass;
import mlda.imbalance.MaxIRIntraClass;
import mlda.imbalance.MaxIRLabelset;
import mlda.imbalance.MeanIRInterClass;
import mlda.imbalance.MeanIRIntraClass;
import mlda.imbalance.MeanIRLabelset;
import mlda.imbalance.MeanStdvIRIntraClass;
import mlda.imbalance.PMax;
import mlda.imbalance.PUniq;
import mlda.labelsDistribution.Cardinality;
import mlda.labelsDistribution.Density;
import mlda.labelsDistribution.MaxEntropy;
import mlda.labelsDistribution.MeanEntropy;
import mlda.labelsDistribution.MinEntropy;
import mlda.labelsDistribution.StdvCardinality;
import mlda.labelsRelation.AvgExamplesPerLabelset;
import mlda.labelsRelation.Bound;
import mlda.labelsRelation.Diversity;
import mlda.labelsRelation.LabelsetsUpTo10Examples;
import mlda.labelsRelation.LabelsetsUpTo2Examples;
import mlda.labelsRelation.LabelsetsUpTo50Examples;
import mlda.labelsRelation.LabelsetsUpTo5Examples;
import mlda.labelsRelation.LabelsetsUpToNExamples;
import mlda.labelsRelation.MeanExamplesPerLabelset;
import mlda.labelsRelation.NumUnconditionalDependentLabelPairsByChiSquare;
import mlda.labelsRelation.ProportionDistinctLabelsets;
import mlda.labelsRelation.RatioLabelsetsUpTo10Examples;
import mlda.labelsRelation.RatioLabelsetsUpTo2Examples;
import mlda.labelsRelation.RatioLabelsetsUpTo50Examples;
import mlda.labelsRelation.RatioLabelsetsUpTo5Examples;
import mlda.labelsRelation.RatioUnconditionalDependentLabelPairsByChiSquare;
import mlda.labelsRelation.SCUMBLE;
import mlda.labelsRelation.StdvExamplesPerLabelset;
import mlda.labelsRelation.UniqueLabelsets;
import mulan.data.InvalidDataFormatException;
import mulan.data.MultiLabelInstances;
import mulan.data.characterizer.Characteristic;
import mulan.data.characterizer.MultilabelCharacteristics;
import mulan.data.characterizer.MultilabelCharacteristics.AbsDifferenceOfCardinality;
import mulan.data.characterizer.MultilabelCharacteristics.AvgExamplesPerClass;
import mulan.data.characterizer.MultilabelCharacteristics.AvgOfDepChiScores;
import mulan.data.characterizer.MultilabelCharacteristics.KurtosisOfTrainCardinality;
import mulan.data.characterizer.MultilabelCharacteristics.LabelCardinalityTest;
import mulan.data.characterizer.MultilabelCharacteristics.LabelCardinalityTrain;
import mulan.data.characterizer.MultilabelCharacteristics.LabelDensityTrain;
import mulan.data.characterizer.MultilabelCharacteristics.MaxOfLabelEntropies;
import mulan.data.characterizer.MultilabelCharacteristics.MeanOfLabelEntropies;
import mulan.data.characterizer.MultilabelCharacteristics.MinOfLabelEntropies;
import mulan.data.characterizer.MultilabelCharacteristics.NumClassesWithUpTo10Examples;
import mulan.data.characterizer.MultilabelCharacteristics.NumClassesWithUpTo2Examples;
import mulan.data.characterizer.MultilabelCharacteristics.NumClassesWithUpTo50Examples;
import mulan.data.characterizer.MultilabelCharacteristics.NumClassesWithUpTo5Examples;
import mulan.data.characterizer.MultilabelCharacteristics.NumOfTestDistinctClasses;
import mulan.data.characterizer.MultilabelCharacteristics.NumOfTrainDistinctClasses;
import mulan.data.characterizer.MultilabelCharacteristics.NumberOfLabels;
import mulan.data.characterizer.MultilabelCharacteristics.RatioClassesWithExamplesLessHalfAttributes;
import mulan.data.characterizer.MultilabelCharacteristics.RatioClassesWithUpTo10Examples;
import mulan.data.characterizer.MultilabelCharacteristics.RatioClassesWithUpTo2Examples;
import mulan.data.characterizer.MultilabelCharacteristics.RatioClassesWithUpTo50Examples;
import mulan.data.characterizer.MultilabelCharacteristics.RatioClassesWithUpTo5Examples;
import mulan.data.characterizer.MultilabelCharacteristics.RatioTestToPower;
import mulan.data.characterizer.MultilabelCharacteristics.RatioTotalToPower;
import mulan.data.characterizer.MultilabelCharacteristics.RatioTrainToPower;
import mulan.data.characterizer.MultilabelCharacteristics.RatioUnseenToTest;
import mulan.data.characterizer.MultilabelCharacteristics.SkewnessOfTrainCardinality;
import mulan.data.characterizer.MultilabelCharacteristics.StDevOfTrainCardinality;
import mulan.data.characterizer.MultilabelCharacteristics.TotalDistinctClasses;
import mulan.data.characterizer.MultilabelCharacteristics.UncondDepPairsNum;
import mulan.data.characterizer.MultilabelCharacteristics.UncondDepPairsRatio;
import mulan.data.characterizer.MultilabelCharacteristics.UnseenInTrain;
import mulan.data.characterizer.StatisticalCharacteristics.AverageAbsoluteCorrelation;
import mulan.data.characterizer.StatisticalCharacteristics.AverageGainRatio;
import mulan.data.characterizer.StatisticalCharacteristics.BinaryAttsRatio;
import mulan.data.characterizer.StatisticalCharacteristics.CategoricalAttsRatio;
import mulan.data.characterizer.StatisticalCharacteristics.DefaultAccuracy;
import mulan.data.characterizer.StatisticalCharacteristics.MeanKurtosis;
import mulan.data.characterizer.StatisticalCharacteristics.MeanOfEntropies;
import mulan.data.characterizer.StatisticalCharacteristics.MeanOfMeans;
import mulan.data.characterizer.StatisticalCharacteristics.MeanOfStDev;
import mulan.data.characterizer.StatisticalCharacteristics.MeanSkewness;
import mulan.data.characterizer.StatisticalCharacteristics.NumOfAttributes;
import mulan.data.characterizer.StatisticalCharacteristics.NumOfBinaryAtts;
import mulan.data.characterizer.StatisticalCharacteristics.NumOfTest;
import mulan.data.characterizer.StatisticalCharacteristics.NumOfTotal;
import mulan.data.characterizer.StatisticalCharacteristics.NumOfTrain;
import mulan.data.characterizer.StatisticalCharacteristics.ProportionWithOutliers;
import mulan.data.characterizer.StatisticalCharacteristics.TestToAttsRatio;
import mulan.data.characterizer.StatisticalCharacteristics.TrainTestRatio;
import mulan.data.characterizer.StatisticalCharacteristics.TrainToAttsRatio;

public class MetaFeaturesPerFold {
	public MultiLabelInstances fold;
	ArrayList<Characteristic> characteristics;
	ArrayList<Characteristic> mutualCharacteristics;
	ArrayList<MLDataMetric> mlDataMetrics;
	static JSONArray jsonArrayFold;
	public MetaFeaturesPerFold(MultiLabelInstances fold) {
		characteristics = new ArrayList<>();
		mutualCharacteristics = new ArrayList<>();
		mlDataMetrics = new ArrayList<>();
		jsonArrayFold = new JSONArray();
		this.fold = fold;
	}
	
//	@SuppressWarnings("unchecked")
//	public void computeOne(Characteristic characteristic) {
//		long start = System.currentTimeMillis();
//		double value = characteristic.compute(this.train, this.test);
//		long end = System.currentTimeMillis();
//		long time = end -start;
//		JSONObject jsonObject = new JSONObject();
//		JSONObject jsonObject2 = new JSONObject();
//		jsonObject2.put("value", value);
//		jsonObject2.put("time", time);
//		jsonObject.put(characteristic.getName(), jsonObject2);
//		jsonArrayTrain.add(jsonObject);
//		jsonArrayTest.add(jsonObject);
//		System.out.println(characteristic.getName()+ " value: "+value+" time: "+time);
//		
//	}
	
	@SuppressWarnings("unchecked")
	public void computeOneMLDA(MLDataMetric mlDataMetric) {
		long start = System.currentTimeMillis();
		double value = mlDataMetric.calculate(this.fold);
		long end = System.currentTimeMillis();
		long time = end -start;
		JSONObject jsonObject = new JSONObject();
		JSONObject jsonObject2 = new JSONObject();
		jsonObject2.put("value", value);
		jsonObject2.put("time", time);
		jsonObject.put(mlDataMetric.getName(), jsonObject2);
		jsonArrayFold.add(jsonObject);
//		System.out.println(mlDataMetric.getName()+ " value: "+value+" time: "+time);
		
	
		
	}
	public void computeAll() {	
		NumOfTotal numOfTotal = new NumOfTotal();
		mutualCharacteristics.add(numOfTotal);
		DefaultAccuracy defaultAccuracy = new DefaultAccuracy();
		characteristics.add(defaultAccuracy);
		
//		NumOfTrainDistinctClasses numOfTrainDistinctClasses = new NumOfTrainDistinctClasses();
//		numOfTrainDistinctClasses.compute(train, test);
//		NumOfTestDistinctClasses numOfTestDistinctClasses = new NumOfTestDistinctClasses();
//		numOfTestDistinctClasses.compute(train, test);
//		
//		TotalDistinctClasses totalDistinctClasses = new TotalDistinctClasses();
//		characteristics.add(totalDistinctClasses);	
//		UnseenInTrain unseenInTrain = new UnseenInTrain();
//		characteristics.add(unseenInTrain);		
//		RatioTrainToPower ratioTrainToPower = new RatioTrainToPower();
//		characteristics.add(ratioTrainToPower);		
//		RatioTestToPower ratioTestToPower = new RatioTestToPower();
//		characteristics.add(ratioTestToPower);
//		RatioTotalToPower ratioTotalToPower = new RatioTotalToPower();
//		characteristics.add(ratioTotalToPower);		
//		RatioUnseenToTest ratioUnseenToTest = new RatioUnseenToTest();
//		characteristics.add(ratioUnseenToTest);
//		
//		for (Characteristic characteristic : characteristics) {
//    			computeOne(characteristic);
//		}
		//end Mulan
				
		//mlda dimensionality
		Attributes attributes = new Attributes();
		mlDataMetrics.add(attributes);
		DistinctLabelsets distinctLabelsets = new DistinctLabelsets();
		mlDataMetrics.add(distinctLabelsets);
		Instances instances = new Instances();
		mlDataMetrics.add(instances);
		Labels labels = new Labels();
		mlDataMetrics.add(labels);
		LxIxF lxixf = new LxIxF();
		mlDataMetrics.add(lxixf);
		RatioInstancesToAttributes rita = new RatioInstancesToAttributes();
		mlDataMetrics.add(rita);
		
		
		//labels distribution metrics 
		Cardinality cardinality = new Cardinality();
		mlDataMetrics.add(cardinality);
		Density density = new Density();
		mlDataMetrics.add(density);
		MaxEntropy maxEntropy = new MaxEntropy();
		mlDataMetrics.add(maxEntropy);
		MeanEntropy meanEntropy = new MeanEntropy();
		mlDataMetrics.add(meanEntropy);
		MinEntropy minEntropy = new MinEntropy();
		mlDataMetrics.add(minEntropy);
		StdvCardinality stdvCardinality = new StdvCardinality();
		mlDataMetrics.add(stdvCardinality);
		
		//imbalance metrics 
		CVIRInterClass cvIRInterClass = new CVIRInterClass();
		mlDataMetrics.add(cvIRInterClass);
		KurtosisCardinality kurtosisCardinality = new KurtosisCardinality();
		mlDataMetrics.add(kurtosisCardinality);
		MaxIRInterClass maxIRInterClass = new MaxIRInterClass();
		mlDataMetrics.add(maxIRInterClass);
		MaxIRIntraClass maxIRIntraClass = new MaxIRIntraClass();
		mlDataMetrics.add(maxIRIntraClass);
		MaxIRLabelset maxIRLavelset = new MaxIRLabelset();
		mlDataMetrics.add(maxIRLavelset);
		MeanIRInterClass meanIRInterClass = new MeanIRInterClass();
		mlDataMetrics.add(meanIRInterClass);
		MeanIRIntraClass meanIRIntraClass = new MeanIRIntraClass();
		mlDataMetrics.add(meanIRIntraClass);
		MeanIRLabelset meanIRLabelset = new MeanIRLabelset();
		mlDataMetrics.add(meanIRLabelset);
		MeanStdvIRIntraClass meanStdvIRIntraClass  = new  MeanStdvIRIntraClass();
		mlDataMetrics.add(meanStdvIRIntraClass);
		PMax pMax = new PMax();
		mlDataMetrics.add(pMax);
		PUniq pUniq = new PUniq();
		mlDataMetrics.add(pUniq);
//		SkewnessCardinality skewnessCardinality = new SkewnessCardinality();
//		mlDataMetrics.add(skewnessCardinality);
		
		
		//labels relation metrics 
		AvgExamplesPerLabelset avgExamplesPerLabelset = new AvgExamplesPerLabelset();
		mlDataMetrics.add(avgExamplesPerLabelset);
		Bound bound = new Bound();
		mlDataMetrics.add(bound);
		Diversity diversity = new Diversity();
		mlDataMetrics.add(diversity);
		LabelsetsUpTo10Examples labelsetsUpTo10Examples = new LabelsetsUpTo10Examples();
		mlDataMetrics.add(labelsetsUpTo10Examples);
		LabelsetsUpTo2Examples labelsetsUpTo2Examples = new LabelsetsUpTo2Examples();
		mlDataMetrics.add(labelsetsUpTo2Examples);
		LabelsetsUpTo50Examples labelsetsUpTo50Examples = new LabelsetsUpTo50Examples();
		mlDataMetrics.add(labelsetsUpTo50Examples);
		LabelsetsUpTo5Examples labelsetsUpTo5Examples = new LabelsetsUpTo5Examples();
		mlDataMetrics.add(labelsetsUpTo5Examples);
		MeanExamplesPerLabelset meanExamplesPerLabelset = new MeanExamplesPerLabelset();
		mlDataMetrics.add(meanExamplesPerLabelset);
		NumUnconditionalDependentLabelPairsByChiSquare numUnconditionalDependentLabelPairsByChiSquare = new NumUnconditionalDependentLabelPairsByChiSquare();
		mlDataMetrics.add(numUnconditionalDependentLabelPairsByChiSquare);
		ProportionDistinctLabelsets proportionDistinctLabelsets = new ProportionDistinctLabelsets();
		mlDataMetrics.add(proportionDistinctLabelsets);
		RatioLabelsetsUpTo10Examples ratioLabelsetsUpTo10Examples = new RatioLabelsetsUpTo10Examples();
		mlDataMetrics.add(ratioLabelsetsUpTo10Examples);
		RatioLabelsetsUpTo2Examples ratioLabelsetsUpTo2Examples = new RatioLabelsetsUpTo2Examples();
		mlDataMetrics.add(ratioLabelsetsUpTo2Examples);
		RatioLabelsetsUpTo50Examples ratioLabelsetsUpTo50Examples = new RatioLabelsetsUpTo50Examples();
		mlDataMetrics.add(ratioLabelsetsUpTo50Examples);
		RatioLabelsetsUpTo5Examples ratioLabelsetsUpTo5Examples = new RatioLabelsetsUpTo5Examples();
		mlDataMetrics.add(ratioLabelsetsUpTo5Examples);
		RatioUnconditionalDependentLabelPairsByChiSquare ratioUnconditionalDependentLabelPairsByChiSquare = new RatioUnconditionalDependentLabelPairsByChiSquare();
		mlDataMetrics.add(ratioUnconditionalDependentLabelPairsByChiSquare);
		SCUMBLE scumble = new SCUMBLE();
		mlDataMetrics.add(scumble);
		StdvExamplesPerLabelset stdvExamplesPerLabelset = new StdvExamplesPerLabelset();
		mlDataMetrics.add(stdvExamplesPerLabelset);
		UniqueLabelsets uniqueLabelsets = new UniqueLabelsets();
		mlDataMetrics.add(uniqueLabelsets);
		
		//attributes
//		AvgAbsoluteCorrelationBetweenNumericAttributes avgAbsoluteCorrelationBetweenNumericAttributes = new AvgAbsoluteCorrelationBetweenNumericAttributes();
//		avgAbsoluteCorrelationBetweenNumericAttributes.calculate(train);
//		mlDataMetrics.add(avgAbsoluteCorrelationBetweenNumericAttributes);
		AvgGainRatio avgGainRatio = new AvgGainRatio();
		mlDataMetrics.add(avgGainRatio);
		BinaryAttributes binaryAttributes = new BinaryAttributes();
		mlDataMetrics.add(binaryAttributes);
		MeanEntropiesNominalAttributes meanEntropiesNominalAttributes = new MeanEntropiesNominalAttributes();
		mlDataMetrics.add(meanEntropiesNominalAttributes);
		mlda.attributes.MeanKurtosis meanKurtosis2 = new mlda.attributes.MeanKurtosis();
		mlDataMetrics.add(meanKurtosis2);
		MeanOfMeanOfNumericAttributes meanOfMeanOfNumericAttributes = new MeanOfMeanOfNumericAttributes();
		mlDataMetrics.add(meanOfMeanOfNumericAttributes);
		MeanSkewnessNumericAttributes meanSkewnessNumericAttributes = new MeanSkewnessNumericAttributes();
		mlDataMetrics.add(meanSkewnessNumericAttributes);
		MeanStdvNumericAttributes meanStdvNumericAttributes = new MeanStdvNumericAttributes();
		mlDataMetrics.add(meanStdvNumericAttributes);
		NominalAttributes nominalAttributes = new NominalAttributes();
		mlDataMetrics.add(nominalAttributes);
		NumericAttributes numericAttributes = new NumericAttributes();
		mlDataMetrics.add(numericAttributes);
		ProportionBinaryAttributes proportionBinaryAttributes = new ProportionBinaryAttributes();
		mlDataMetrics.add(proportionBinaryAttributes);
		ProportionNominalAttributes proportionNominalAttributes = new ProportionNominalAttributes();
		mlDataMetrics.add(proportionNominalAttributes);
		ProportionNumericAttributes proportionNumericAttributes = new ProportionNumericAttributes();
		mlDataMetrics.add(proportionNumericAttributes);
		ProportionNumericAttributesWithOutliers proportionNumericAttributesWithOutliers = new ProportionNumericAttributesWithOutliers();
		mlDataMetrics.add(proportionNumericAttributesWithOutliers);
		 
		System.out.println("---------------MLDA");
		for (MLDataMetric mlDataMetric : mlDataMetrics) {
			computeOneMLDA(mlDataMetric);
		}
		
	}
	
	public void saveToJson(String datasetName) throws IOException {
		FileWriter file = new FileWriter("D:/MLC/MetafeaturesPerFold/"
						+ datasetName + ".json"); 
		file.write(jsonArrayFold.toJSONString());
		file.close();
		
		
	}
	public static void main(String[] args) throws InvalidDataFormatException, IOException {
				
		
		File directory = new File("D:/MLC/Datasets-ARFF-Fold");
		for (File dataset: directory.listFiles()) {
			String xmlLoc = "D:/MLC/XML/"+dataset.getName()+"/"+dataset.getName()+".xml";
			for(File fold: dataset.listFiles()) {
				System.out.println("------------Start-Dataset: "+fold.getName());
				MultiLabelInstances foldMLI = new MultiLabelInstances(fold.getAbsolutePath(), xmlLoc);
				MetaFeaturesPerFold mf = new MetaFeaturesPerFold(foldMLI);
	 			mf.computeAll();
	 			mf.saveToJson(fold.getName().split("\\.")[0]);
	 			System.out.println("----------------------------------------End-Dataset: "+fold.getName());
			}
		}
//		for (String folder : directory.list()) {
//			if(folder.equals("XMLS")||folder.equals("settings")) continue;
//			System.out.println("----------------------------------------Start-Dataset: "+folder);
// 			MultiLabelInstances train = new MultiLabelInstances("C:\\Users\\ana\\Desktop\\RepoSemanticDatasets\\MLC_datasets_new\\MULAN\\"+folder+"\\train\\"+folder+"_train.arff", "C:\\Users\\ana\\Desktop\\RepoSemanticDatasets\\MLC_datasets_new\\MULAN\\"+folder+"\\"+folder+".xml");
// 			MultiLabelInstances test = new MultiLabelInstances("C:\\Users\\ana\\Desktop\\RepoSemanticDatasets\\MLC_datasets_new\\MULAN\\"+folder+"\\test\\"+folder+"_test.arff","C:\\Users\\ana\\Desktop\\RepoSemanticDatasets\\MLC_datasets_new\\MULAN\\"+folder+"\\"+folder+".xml");
// 			MetaFeaturesMulanMlda mf = new MetaFeaturesMulanMlda(train, test);
// 			mf.computeAll();
// 			mf.saveToJson(folder);
// 			System.out.println("----------------------------------------End-Dataset: "+folder);
//
//		}
		
		
		
	}

}
