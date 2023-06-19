package clus;

import java.io.UnsupportedEncodingException;
import java.security.MessageDigest;
import java.security.NoSuchAlgorithmException;

import javax.xml.bind.DatatypeConverter;

import org.apache.jena.rdf.model.Model;
import org.apache.jena.rdf.model.Resource;
import org.apache.jena.vocabulary.RDF;
import org.apache.jena.vocabulary.RDFS;

import com.google.gson.JsonArray;
import com.google.gson.JsonElement;
import com.google.gson.JsonObject;

public class Annotator {
	Model model;
	String URIprefix;

	public Annotator(Model model, String URIprefix) {
		this.model = model;
		this.URIprefix = URIprefix;
	}

	public String findURI(JsonArray ja, String label) {
		for (JsonElement jsonElement : ja) {
			JsonObject jo = (JsonObject) jsonElement;
			JsonElement idJson = jo.get("@id");
			String id = idJson.toString().replace("\"", "");
			JsonArray labelArray = (JsonArray) jo.get("http://www.w3.org/2000/01/rdf-schema#label");
			if (labelArray != null) {
				JsonObject labelJson = (JsonObject) labelArray.get(0);
				if (labelJson != null) {
					String labelValue = labelJson.get("@value").toString().replace("\"", "");
					if (labelValue != null && labelValue.equals(label)) {
						return id;
					}
				}
			}
		}
		return null;
	}

	Resource createResource(Resource type, String label) {
		Resource newResource = model.createResource(URIprefix + stringToHash(label));
		if (type != null) {
			newResource.addProperty(RDF.type, type);
		}
		if (label != null) {
			newResource.addProperty(RDFS.label, label);
		}
		return newResource;
	}
	
	Resource createResourceString(String typeURL, String label) {
		Resource typeResource;
		Resource newResource = model.createResource(URIprefix + stringToHash(label));
		if(model.getResource(typeURL)!=null) {
			//already exists
			typeResource = model.getResource(typeURL);
		}
		else {
			//create the resource 
			typeResource = model.createResource(typeURL);
		}
		if (typeURL != null) {
			newResource.addProperty(RDF.type, typeResource);
		}
		if (label != null) {
			newResource.addProperty(RDFS.label, label);
		}
		return newResource;
	}

	public String stringToHash(String name) {
		String hash = "";
		try {
			hash = DatatypeConverter.printHexBinary(MessageDigest.getInstance("MD5").digest(name.getBytes("UTF-8")));
		} catch (NoSuchAlgorithmException e) {
			e.printStackTrace();
		} catch (UnsupportedEncodingException e) {
			e.printStackTrace();
		}
		return hash;
	}
	
	public Resource getResourceFromModel(org.apache.jena.rdf.model.Model modelJena, String label) {
		Resource resource = modelJena.listResourcesWithProperty(RDFS.label, label).next();
		return resource;
	}

}
