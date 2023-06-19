package clus;

import java.io.BufferedReader;
import java.io.File;
import java.io.FileNotFoundException;
import java.io.FileReader;
import java.io.FileWriter;
import java.io.IOException;
import java.util.Arrays;

public class CleanArffs {
	public static void cleanFile(String datasetName, String mode) throws IOException {
		System.out.println(datasetName+" "+mode+" started");
		String fileName = "C:\\Users\\ana\\Google Drive\\bookChapter\\Clus3\\MF-datasets\\" + datasetName + "\\" + mode
				+ "\\" + datasetName + "_" + mode + "_original.arff";
		String line = null;
		boolean data = false;
		FileReader fileReader = new FileReader(fileName);
		BufferedReader bufferedReader = new BufferedReader(fileReader);
		String fileNameLong = "C:\\Users\\ana\\Google Drive\\bookChapter\\Clus3\\MF-datasets\\" + datasetName + "\\" + mode
				+ "\\" + datasetName + "_" + mode + ".arff";
		FileWriter fw = new FileWriter(fileNameLong);

		
		while ((line = bufferedReader.readLine()) != null) {
			if (line.equals("@data")) {
				data = true;
				fw.write("\n");
				fw.write(line+"\n");
				fw.flush();
				continue;
			}
			if (data) {
				StringBuilder newLine = new StringBuilder();
				line = line.replace("{", "");
				line = line.replace("}", "");
				String [] lineParts = line.split(",");
				int lastIdx = Integer.parseInt(lineParts[lineParts.length-1].split(" ")[0]);
				int [] lineArray = new int[lastIdx];
				Arrays.fill(lineArray, 0);
				for(int i = 0; i<lineParts.length; i++) {
					String [] tuple = lineParts[i].split(" ");
					int index = Integer.parseInt(tuple[0]);
					int value = Integer.parseInt(tuple[1]);
					lineArray[index-1] = value;
				}
				for(int j = 0; j<lineArray.length; j++) {
					newLine = newLine.append(lineArray[j]);
					if(j<lineArray.length-1) {
						newLine = newLine.append(",");
					}
				}
				newLine = newLine.append("\n");
				fw.write(newLine.toString());
				fw.flush();
			}
			else {
				fw.write(line+"\n");
				fw.flush();
			}

		}
		bufferedReader.close();		
		fw.close();
		
	}

	public static void main(String[] args) throws IOException {
//		String[] datasets = { "Arts1", "Business1", "Computers1", "Education1", "Entertainment1", "Health1", "Recreation1", "Reference1", "Science1", "Social1", "Society1"};
		String [] datasets = {"Arts1"}; 
		for(String dataset: datasets) {
			cleanFile(dataset, "train");
			cleanFile(dataset, "test");
		}
		

	}

}
