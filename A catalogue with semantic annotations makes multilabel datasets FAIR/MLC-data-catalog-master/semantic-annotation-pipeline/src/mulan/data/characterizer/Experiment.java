package mulan.data.characterizer;

import mulan.data.MultiLabelInstances;
import weka.core.TechnicalInformation;
import weka.core.Utils;

import java.io.BufferedWriter;
import java.io.File;
import java.io.FileWriter;
import java.io.IOException;

public class Experiment {

    static StringBuilder sb1 = new StringBuilder();

    public static void main(String[] args) throws Exception {

        Runtime r = Runtime.getRuntime();
        String separator = File.separator;
        long start, end;
        long time;
        Characterizer dataCharacterizer = new Characterizer();
        dataCharacterizer.addMeasures(StatisticalCharacteristics.class);
        dataCharacterizer.addMeasures(MultilabelCharacteristics.class);
        File resultsFolder = new File("dataset-characteristics" + separator);
        if (!resultsFolder.exists()) resultsFolder.mkdirs();
        sb1.append("dataset;").append(dataCharacterizer.namesToCSV()).append("\n");

        String dataFolder = Utils.getOption("path", args);                //e.g. -path "D:\\meta-experiment\\manipulated-data\\"
        String xmlFolder =  Utils.getOption("xml", args);                   //e.g. -xml "D:\\meta-experiment\\manipulated-data\\"
        String resFileName = Utils.getOption("sF", args);                 //e.g. -sF "\\results.txt"
        String dataSetsArg = Utils.getOption("datasets", args);   //e.g. -datasets "emotions scene yeast"
        String[] dataSetsToRun =  Utils.splitOptions(dataSetsArg);

        for (String dataSet : dataSetsToRun) {
            System.out.println("\nStarting dataset " + dataSet);
            File trainDir = new File(dataFolder,dataSet + separator +"train" + separator);
            File testDir = new File(dataFolder,dataSet + separator + "test" + separator);
            System.out.println("trainDir = " + trainDir);
            File[] trainFiles = trainDir.listFiles();
            System.out.println(" contains : " + trainFiles.length + " files.");
            for(File file : trainFiles){
                String trainFileName = file.getName();
                String testFileName = trainFileName.replaceAll("train", "test");
                String path = xmlFolder + dataSet + separator;
                String filestem = dataSet;
                System.out.println("Loading the training set " + trainFileName);
                MultiLabelInstances train = new MultiLabelInstances(trainDir.getPath() + separator + trainFileName  , path + filestem + ".xml");
                System.out.println("Loading the test set " + testFileName);
                MultiLabelInstances test = new MultiLabelInstances(testDir.getPath() + separator + testFileName,  path + filestem + ".xml");
                sb1.append(trainFileName + ';');
                StatisticalCharacteristics.reset();
                MultilabelCharacteristics.reset();
                start= System.currentTimeMillis();
                dataCharacterizer.calculate(train,test);
                end = System.currentTimeMillis();
                time = end -start;
                sb1.append(dataCharacterizer.toCSV()).append('\n');
                addToFile(resultsFolder + resFileName,sb1);
                sb1.setLength(0);
                System.out.println(dataCharacterizer);
                System.out.println("Computation time: " + time + " millisec. =  " + (double)time / 1000 + " sec.");
            }
        }
    }

    public static void addToFile(String name, StringBuilder stringBuilder) {
        BufferedWriter out;
        try {
            FileWriter fr = new FileWriter(name, true);
            out = new BufferedWriter(fr);
            System.out.println("Writing to file: " + name);
            out.write(stringBuilder.toString());
            out.close();
        } catch (IOException e) {
            e.printStackTrace();
        }
    }
   
    public TechnicalInformation getTechnicalInformation() {
        		TechnicalInformation result;
		result = new TechnicalInformation(TechnicalInformation.Type.INPROCEEDINGS);
		result.setValue(TechnicalInformation.Field.AUTHOR,
				"Lena Chekina (nee Tenenboim), Lior Rokach, and Bracha Shapira");
		result.setValue(TechnicalInformation.Field.TITLE,
				"Meta-Learning for Selecting a Multi-Label Classification Algorithm");
		result.setValue(TechnicalInformation.Field.VOLUME,
				"Proc. ICDM 2011 Workshop on Optimization based Techniques for Emerging Data Mining Problems");
		result.setValue(TechnicalInformation.Field.YEAR, "2011");
		result.setValue(TechnicalInformation.Field.ADDRESS, "Vancouver, Canada");
		return result;
    }


}