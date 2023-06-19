package clus;

import java.io.BufferedReader;
import java.io.FileNotFoundException;
import java.io.FileReader;
import java.io.FileWriter;
import java.io.IOException;
import java.io.InputStreamReader;
import java.io.PrintStream;
import java.util.Iterator;
import java.util.Map.Entry;

import org.apache.jena.ontology.OntModel;
import org.apache.jena.ontology.OntModelSpec;
import org.apache.jena.ontology.OntProperty;
import org.apache.jena.rdf.model.Model;
import org.apache.jena.rdf.model.ModelFactory;
import org.apache.jena.rdf.model.Resource;
import org.apache.jena.riot.RDFDataMgr;
import org.apache.jena.riot.RDFFormat;
import org.json.simple.JSONArray;
import org.json.simple.JSONObject;

import com.google.gson.JsonArray;
import com.google.gson.JsonElement;
import com.google.gson.JsonIOException;
import com.google.gson.JsonParser;
import com.google.gson.JsonSyntaxException;

import clus.util.ClusException;

public class MetaFeatures {
	public String URIprefix = "http://ontodm.com/SemanticAnnotation#";
	public Model model;
	public JsonArray ontologyJson;
	public Annotator ann;
	public OntProperty hasValue;
	public OntProperty hasQuality;
	public OntProperty typeName;

	public void addProperties() {
		OntModel ontModel = ModelFactory.createOntologyModel(OntModelSpec.OWL_DL_MEM);
		hasValue = ontModel.createDatatypeProperty("http://www.ontodm.com/OntoDT#OntoDT_0000240");
		hasQuality = ontModel.createObjectProperty("http://purl.obolibrary.org/obo/RO_0000086");
		typeName = ontModel.createDatatypeProperty(URIprefix + "typeName");
		model.add(ontModel);
	}

	public MetaFeatures(Model model) {
		this.model = model;
		this.ann = new Annotator(this.model, URIprefix);
	}

	public void generateMetaFeatures(JsonArray json, String datasetName, Resource dsetResource, String dspec)
			throws FileNotFoundException {
		String dsetLabel = "dset:" + datasetName + "-" + "MLC" + "-" + dspec;
		System.out.println("DSET: " + dsetLabel);
		for (int i = 0; i<json.size(); i++) {
			JsonElement entry = json.get(i);
			Iterator<Entry<String, JsonElement>> it = entry.getAsJsonObject().entrySet().iterator();
			Entry<String, JsonElement> a = it.next(); 
			String metaFeatureLabel = a.getKey();
			JsonElement metaFeatureValue = a.getValue().getAsJsonObject().get("value");
			JsonElement time = a.getValue().getAsJsonObject().get("time");
//			System.out.println("key: "+metaFeatureLabel+" value: "+metaFeatureValue);
//			System.out.println("p: "+ann.findURI(ontologyJson, metaFeatureLabel));
			Resource ontoMetaFeature = this.model.createResource(ann.findURI(ontologyJson, metaFeatureLabel));
//			System.out.println(metaFeatureLabel+" : "+ontoMetaFeature);
			Resource metaFeatureResource = ann.createResource(ontoMetaFeature, dsetLabel + "-" + metaFeatureLabel);
			metaFeatureResource.addLiteral(hasValue, metaFeatureValue).addLiteral(typeName,
					metaFeatureLabel);
			dsetResource.addProperty(hasQuality, metaFeatureResource);
		}
//		PrintStream bw = new PrintStream("C:\\Users\\ana\\Desktop\\bookChapter\\TripleStore\\separateRDFs//results_" + datasetName + ".rdf");
//		RDFDataMgr.write(bw, model, RDFFormat.RDFXML);

	}

	public void metaFeaturesMLC(String datasetName, Resource resource, String dspec)
			throws JsonIOException, JsonSyntaxException, IOException, InterruptedException {
		Object obj = new JsonParser().parse(new FileReader(
				"C:\\Users\\ana\\Google Drive\\DS-ontologies\\ontodm-core\\development_version\\OntoDM-metaFeaturesMergedLD.owl"));
		this.ontologyJson = (JsonArray) obj;
		this.addProperties();

		System.out.println("metaFeatures annotation of "+datasetName);
		
		Object mf = new JsonParser().parse(new FileReader(
				"C:\\Users\\ana\\Desktop\\RepoSemanticDatasets\\e8datasets-master\\MLC\\metaFeaturesJsonFiles\\" 	+ datasetName + "_train.json"));
		JsonArray json = (JsonArray) mf;
		this.generateMetaFeatures(json, datasetName, resource, dspec);
	}

	public static void main(String[] args) throws IOException, ClusException, InterruptedException {
		//FOR CALCULATION OF THE META FEATURES GO TO mlda.run
	}

}
