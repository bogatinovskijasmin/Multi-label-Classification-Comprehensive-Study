package clus;

import java.io.File;
import java.io.FileNotFoundException;
import java.io.FileReader;
import java.io.PrintStream;
import java.io.UnsupportedEncodingException;
import java.security.MessageDigest;
import java.security.NoSuchAlgorithmException;

import javax.xml.bind.DatatypeConverter;

import org.apache.jena.ontology.OntModel;
import org.apache.jena.ontology.OntModelSpec;
import org.apache.jena.ontology.OntProperty;
import org.apache.jena.rdf.model.Model;
import org.apache.jena.rdf.model.ModelFactory;
import org.apache.jena.rdf.model.Resource;
import org.apache.jena.riot.RDFDataMgr;
import org.apache.jena.riot.RDFFormat;
import org.apache.jena.vocabulary.RDF;
import org.apache.jena.vocabulary.RDFS;

import com.google.gson.JsonArray;
import com.google.gson.JsonElement;
import com.google.gson.JsonIOException;
import com.google.gson.JsonObject;
import com.google.gson.JsonParser;
import com.google.gson.JsonSyntaxException;

public class ProvenanceInformation {
	public String URIprefix = "http://ontodm.com/SemanticAnnotation#";
	public Model model;
	public Annotator ann;
	OntProperty sameAs;
	OntProperty keywords;
	OntProperty identifier;
	OntProperty creator;
	OntProperty url;
	OntProperty name;
	OntProperty description;
	Resource personResource;
	Resource DM_dataset;
	public void addProperties() {
		OntModel ontModel = ModelFactory.createOntologyModel(OntModelSpec.OWL_DL_MEM);
		sameAs = ontModel.createAnnotationProperty("https://schema.org/sameAs");
		keywords = ontModel.createAnnotationProperty("https://schema.org/keywords");
		identifier = ontModel.createAnnotationProperty("https://schema.org/identifier");
		creator = ontModel.createObjectProperty("https://schema.org/creator");
		url = ontModel.createAnnotationProperty("https://schema.org/url");
		name = ontModel.createAnnotationProperty("https://schema.org/name");
		description = ontModel.createAnnotationProperty("https://schema.org/description");
		personResource = model.createResource("https://schema.org/person");
		DM_dataset = model.createResource("http://www.ontodm.com/OntoDM-core/OntoDM_000144");
		model.add(ontModel);
		
	}
	
	public ProvenanceInformation(Model model) {
		this.model = model;
		this.ann = new Annotator(this.model, URIprefix);
	}
	
	public void annotateProvenance(Resource datasetResource, String datasetName) throws JsonIOException, JsonSyntaxException, FileNotFoundException {
		Object obj = new JsonParser().parse(new FileReader(
				"C:\\Users\\ana\\Desktop\\RepoSemanticDatasets\\Clus3\\DescriptionsJsons\\"+datasetName+".json"));
		JsonObject provenanceJson = (JsonObject) obj;
		
		//annotate description
		String descriptionLiteral = provenanceJson.get("description").getAsString();
		datasetResource.addLiteral(description, descriptionLiteral);
		
		//annotate dataset name
		String nameLiteral = provenanceJson.get("name").getAsString();
		datasetResource.addLiteral(name, nameLiteral);
		
		//annotate keywords
		JsonArray keywordsArray = provenanceJson.get("keywords").getAsJsonArray();
		StringBuilder keywordsLiteral = new StringBuilder();
		for (JsonElement keywordElement : keywordsArray) {
			if(!keywordsLiteral.toString().equals("")) keywordsLiteral.append(", ");
			keywordsLiteral.append(keywordElement.getAsString());
		}
		datasetResource.addLiteral(keywords, keywordsLiteral.toString());
		
		//annotate sameAs
		JsonArray sameAsArray = provenanceJson.get("sameAs").getAsJsonArray();
		for (JsonElement sameAsElement : sameAsArray) {
			datasetResource.addLiteral(sameAs, sameAsElement.getAsString());
		}
		
		//annotate identifier
		JsonArray identifierArray = provenanceJson.get("identifier").getAsJsonArray();
		for (JsonElement identifierElement : identifierArray) {
			String idenStr = identifierElement.getAsString();
			if(!idenStr.equals("NA"))
				datasetResource.addLiteral(identifier, identifierElement.getAsString());
		}
		
		//annotate creators 
		JsonArray creatorArray = provenanceJson.get("creator").getAsJsonArray();
		for (JsonElement creatorElement : creatorArray) {
			String creatorURI = creatorElement.getAsJsonObject().get("url").getAsString();
			String creatorName = creatorElement.getAsJsonObject().get("name").getAsString();
			
			Resource creatorResource = ann.createResource(personResource, datasetName+":"+creatorName);
			creatorResource.addLiteral(url, creatorURI);
			creatorResource.addLiteral(name, creatorName);	
			datasetResource.addProperty(creator, creatorResource);
		}
		
	}

	public static void main(String[] args) throws JsonIOException, JsonSyntaxException, FileNotFoundException {			
		ProvenanceInformation pInfo = new ProvenanceInformation(ModelFactory.createDefaultModel());
		pInfo.addProperties();
		File directory = new File("C:\\Users\\ana\\Desktop\\RepoSemanticDatasets\\Clus3\\DescriptionsJsons");
		for (String folder : directory.list()) {
			String datasetName = folder.split("\\.")[0];
			System.out.println(datasetName);
			Resource datasetResource = pInfo.ann.createResource(null, datasetName + "_dataset");
			datasetResource.addProperty(RDFS.subClassOf, pInfo.DM_dataset);
			String task = "MLC";
			String dsetSpec = "supervised";
			String dsetLabel = "dset:" + datasetName + "-" + task + "-" + dsetSpec;
			Resource dsetResource = pInfo.ann.createResource(datasetResource, dsetLabel);
			System.out.println(dsetResource);
			pInfo.annotateProvenance(dsetResource, datasetName);
		}
		PrintStream bw = new PrintStream("C:\\Users\\ana\\Desktop\\RepoSemanticDatasets\\TripleStore\\provenanceMLC"
				+ ".rdf");
		RDFDataMgr.write(bw, pInfo.model, RDFFormat.RDFXML);
		System.out.println("done");
	}

}
