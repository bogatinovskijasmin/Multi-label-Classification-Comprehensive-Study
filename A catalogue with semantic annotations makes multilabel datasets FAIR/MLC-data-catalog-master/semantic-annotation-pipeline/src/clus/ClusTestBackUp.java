/*************************************************************************
 * Clus - Software for Predictive Clustering *
 * Copyright (C) 2007 *
 * Katholieke Universiteit Leuven, Leuven, Belgium *
 * Jozef Stefan Institute, Ljubljana, Slovenia *
 * *
 * This program is free software: you can redistribute it and/or modify *
 * it under the terms of the GNU General Public License as published by *
 * the Free Software Foundation, either version 3 of the License, or *
 * (at your option) any later version. *
 * *
 * This program is distributed in the hope that it will be useful, *
 * but WITHOUT ANY WARRANTY; without even the implied warranty of *
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the *
 * GNU General Public License for more details. *
 * *
 * You should have received a copy of the GNU General Public License *
 * along with this program. If not, see <http://www.gnu.org/licenses/>. *
 * *
 * Contact information: <http://www.cs.kuleuven.be/~dtai/clus/>. *
 *************************************************************************/

package clus;

import java.io.FileNotFoundException;
import java.io.FileReader;
import java.io.IOException;
import org.apache.jena.query.Query;
import org.apache.jena.query.QueryFactory;
import org.apache.jena.query.ResultSetFormatter;
import org.apache.jena.rdf.model.Model;
import org.apache.jena.rdf.model.ModelFactory;
import org.apache.jena.rdf.model.Property;
import org.apache.jena.rdf.model.Resource;
import org.apache.jena.rdfconnection.RDFConnection;
import org.apache.jena.rdfconnection.RDFConnectionFactory;
import org.apache.jena.riot.RDFDataMgr;
import org.apache.jena.riot.RDFFormat;
import org.apache.jena.system.Txn;
import org.apache.jena.vocabulary.RDF;
import org.apache.jena.vocabulary.RDFS;
import org.json.simple.JSONObject;
import org.json.simple.parser.JSONParser;
import org.json.simple.parser.ParseException;

import java.io.File;
import java.io.PrintStream;
import java.io.UnsupportedEncodingException;
import java.security.MessageDigest;
import java.security.NoSuchAlgorithmException;
import javax.xml.bind.DatatypeConverter;

import clus.data.rows.RowData;
import clus.data.type.ClusAttrType;
import clus.data.type.ClusSchema;
import clus.data.type.NominalAttrType;
import clus.jeans.util.cmdline.CMDLineArgs;
import clus.jeans.util.cmdline.CMDLineArgsProvider;
import clus.main.Settings;
import clus.util.ClusException;

public class ClusTestBackUp implements CMDLineArgsProvider {
	public static String URIprefix ="http://ontodm.com/SemanticAnnotation#";
	public static Model model = ModelFactory.createDefaultModel();
	public static Resource DM_dataset = model.createResource("http://ontodm.com/OntoDT#OntoDT_150012/OntoDM_000144").addProperty(RDFS.label, "DM-dataset");
	public static Resource recordDatatype = model.createResource("http://ontodm.com/OntoDT#OntoDT_950419").addProperty(RDFS.label, "record (tuple) datatype");
	public static Resource targetFC = model.createResource("http://www.ontodm.com/OntoDT#OntoDT_0000397").addProperty(RDFS.label, "target field component");
	public static Resource fieldIdentifier = model.createResource("http://ontodm.com/OntoDT#OntoDT_inst_507131").addProperty(RDFS.label, "field identifier");
	public static Resource recordOfPrimitiveDatatype = model.createResource("http://ontodm.com/OntoDT#OntoDT_521859").addProperty(RDFS.label, "record of primitives datatype");
	public static Resource fieldComponent = model.createResource("http://ontodm.com/OntoDT#OntoDT_059114").addProperty(RDFS.label, "field component");
	public static Resource discreteDatatype = model.createResource("http://ontodm.com/OntoDT#OntoDT_608148").addProperty(RDFS.label, "discrete datatype");
	public static Resource discreteValueList = model.createResource("http://ontodm.com/OntoDT#OntoDT_089686").addProperty(RDFS.label, "discrete value list");
	public static Resource discreteValueIdentifier = model.createResource("http://ontodm.com/OntoDT#OntoDT_467794").addProperty(RDFS.label, "discrete value identifier");
	public static Resource realDatatype = model.createResource("http://ontodm.com/OntoDT#OntoDT_150012").addProperty(RDFS.label, "real datatype");
	public static Resource booleanDatatype = model.createResource("http://www.ontodm.com/OntoDT#OntoDT_0000002").addProperty(RDFS.label, "boolean datatype");
	public static Resource setOfDiscreteDatatype = model.createResource("http://ontodm.com/OntoDT#OntoDT_377271").addProperty(RDFS.label, "set of discrete");
	public static Resource discreteBaseType = model.createResource("http://ontodm.com/OntoDT#OntoDT_339518").addProperty(RDFS.label, "discrete base type");
	public static Resource recordOfBooleanDatatype = model.createResource("http://ontodm.com/OntoDT#OntoDT_360708").addProperty(RDFS.label, "record of boolean");
	public static Resource recordOfRealDatatype = model.createResource("http://ontodm.com/OntoDT#OntoDT_471356").addProperty(RDFS.label, "record of real datatype");
	public static Resource recordOfDiscreteDatatype = model.createResource("http://ontodm.com/OntoDT#OntoDT_595741").addProperty(RDFS.label, "record of discrete ");
	
	
	public static Property is_about = model.createProperty("http://purl.obolibrary.org/obo/IAO_0000136");
	public static Property hasMember = model.createProperty("http://semanticscience.org/resource/SIO_000059");
	public static Property hasIdentifier = model.createProperty("http://semanticscience.org/resource/SIO_000671");
	public static Property datatypeRoleOf = model.createProperty("http://ontodm.com/OntoDT#OntoDT_0000010");
	public static Property numberOfInstances = model.createProperty(URIprefix+ "numberOfInstances");
	public static Property nameDataset = model.createProperty(URIprefix + "nameDataset");
	public static Property hasFieldComponent = model.createProperty("http://www.ontodm.com/OntoDT/OntoDT_80000000");
	public static Property hasPart = model.createProperty("http://www.obofoundry.org/ro/ro.owl#has_part");
	public static Property hasBaseDatatype = model.createProperty("http://www.ontodm.com/OntoDT/OntoDT_80000004");
	public static Property hasAlternativeComponent = model.createProperty("http://www.ontodm.com/OntoDT/OntoDT_80000001");
	
	
	
	public static void addPropertyLabels(){
		is_about.addProperty(RDFS.label, "is-about");
		hasMember.addProperty(RDFS.label, "has_member");
		hasIdentifier.addProperty(RDFS.label, "has_identifier");
		datatypeRoleOf.addProperty(RDFS.label, "datatype_role_of");
		numberOfInstances.addProperty(RDFS.label, "number of instances");
		nameDataset.addProperty(RDFS.label, "dataset name");
		hasFieldComponent.addProperty(RDFS.label, "has_field_component");
		hasPart.addProperty(RDFS.label, "has_part");
	}
	
	
	
	@Override
	public String[] getOptionArgs() {
		return null;
	}

	@Override
	public int[] getOptionArgArities() {
		return null;
	}

	@Override
	public int getNbMainArgs() {
		return 0;
	}

	@Override
	public void showHelp() {

	}

	public static String stringToHash(String name) {
		String hash = "";
		try {
			hash = DatatypeConverter
					.printHexBinary(MessageDigest.getInstance("SHA-256").digest(name.getBytes("UTF-8")));
		} catch (NoSuchAlgorithmException e) {
			e.printStackTrace();
		} catch (UnsupportedEncodingException e) {
			e.printStackTrace();
		}
		return hash;
	}

	public static void uploadRdfToServer(String serverPath, String destinationFileName, String sourcePath) {
		RDFConnection conn = RDFConnectionFactory.connect(serverPath);
		System.out.println("Upload a file to Fuseki");
		try {
			Txn.executeWrite(conn, () -> {
				conn.load(serverPath + "/data/" + destinationFileName, sourcePath);
			});
			System.out.println("File upload successful");
		} catch (Exception e) {
			e.printStackTrace();
			System.out.println("File upload failed");
		} finally {
		}
	}

	public static void executeQuery(String server, String queryString) {
		Query query = QueryFactory.create(queryString);
		try (RDFConnection conn = RDFConnectionFactory.connect(server)) {
			conn.queryResultSet(query, ResultSetFormatter::out);
		} catch (Exception e) {
			e.printStackTrace();
		} finally {
		}
	}
	
	public static void discreteDatatype (Resource resourceDiscreteDatatype, String spec, String attrName,  String [] components){
		String DiscreteListLabel = attrName + "-dis-list:"  + spec;
		String DisListURI = URIprefix + stringToHash(DiscreteListLabel);
		// descDtypeAttDisList instance_of discrete-value-list
		Resource DisListResource = model.createResource(DisListURI)
				.addProperty(RDFS.label, DiscreteListLabel)
				.addProperty(RDF.type, discreteValueList);
		
		// descDtypeAttType has_member descDtypeAttDisList
		resourceDiscreteDatatype.addProperty(hasMember, DisListResource);
		for (int i = 0; i < components.length; i++) {
			String component = components[i];
			int num = i + 1;
			String AttComponent = attrName + "DiscreteValueIdentifier" + num+ ":"+  spec;
			String AttComponentURI = URIprefix + stringToHash(AttComponent);
			// AttComponent instance_of discrete value identifier
			Resource AttComponentResource = model.createResource(AttComponentURI)
					.addProperty(RDFS.label,  spec + "|" + attrName + ":" + component)
					.addProperty(RDF.type, discreteValueIdentifier);
			// descDtypeAttDisList has-member AttComponent
			DisListResource.addProperty(hasMember, AttComponentResource);
		}
		
	}
	
	public static void recordOfComplex(Resource recordResource, Resource [] complexResources, String [] components, String extention, Resource FC){
		//We can use this function for record of real, record of primitives, record of boolean.. 
				for (int i = 0; i<components.length; i++){
					String fieldComponentLabel = components[i]+"FC:"+extention;
					String fieldComponentURI = URIprefix + stringToHash(fieldComponentLabel);
					Resource fieldComponentResource = model.createResource(fieldComponentURI).addProperty(RDFS.label, fieldComponentLabel).addProperty(RDF.type, FC);
					recordResource.addProperty(hasFieldComponent, fieldComponentResource);
					
					String fieldIDLabel = components[i]+"ID:"+extention;
					String fieldIDURI = URIprefix + stringToHash(fieldIDLabel);
					Resource fieldIDResource = model.createResource(fieldIDURI).addProperty(RDFS.label, fieldIDLabel).addProperty(RDF.type, fieldIdentifier);
					fieldComponentResource.addProperty(hasIdentifier, fieldIDResource);
					
					fieldComponentResource.addProperty(datatypeRoleOf, complexResources[i]);
					
				}
	}
	
	public static void recordOfSomething(Resource recordResource, String [] components, String componentType, String spec, String FC){
		//Before calling the function recordResource must have the type specified, as well as its label
		//We can use this function for record of real, record of primitives, record of boolean.. 
		for (String component : components) {
			String fieldComponentLabel = component+"FC:"+ spec;
			String fieldComponentURI = URIprefix + stringToHash(fieldComponentLabel);
			Resource fieldComponentResource = model.createResource(fieldComponentURI).addProperty(RDFS.label, fieldComponentLabel).addProperty(RDF.type, FC);
			recordResource.addProperty(hasFieldComponent, fieldComponentResource);
			
			String fieldIDLabel = component+"ID:"+ spec;
			String fieldIDURI = URIprefix + stringToHash(fieldIDLabel);
			Resource fieldIDResource = model.createResource(fieldIDURI).addProperty(RDFS.label, fieldIDLabel).addProperty(RDF.type, fieldIdentifier);
			fieldComponentResource.addProperty(hasIdentifier, fieldIDResource);
			
			String componentDataTypeLabel = component+"DataType:"+ spec;
			String componentDataTypeURI = URIprefix + stringToHash(componentDataTypeLabel);
			Resource componentDataTypeURIResource = model.createResource(componentDataTypeURI).addProperty(RDFS.label, componentDataTypeLabel).addProperty(RDF.type, componentType);
			fieldComponentResource.addProperty(datatypeRoleOf, componentDataTypeURIResource);
			
		}
	}
	public static String [] getDiscreteComponentsForAttribute(ClusAttrType attribute){
		NominalAttrType nomT = (NominalAttrType) attribute;
		String value = nomT.getTypeString();
		String[] components = getComponents(value);
		return components;
	}

	public static void createDatasetAnnotations(String[] args, String tdbLocation, String rdfName, JSONObject json) throws IOException, ClusException {
		Clus clus = new Clus();
		Settings sett = clus.getSettings();
		CMDLineArgs cargs = new CMDLineArgs(clus);
		cargs.process(args);
		if (cargs.allOK()) {
			sett.setAppName(cargs.getMainArg(0));
			clus.initSettings(cargs);

			clus.initialize(cargs);
		}
		
		RowData data = clus.getData();
		ClusSchema schema = data.getSchema();	
		boolean hasMissing = schema.hasMissing();                        
		
		String datasetName = args[0].replaceFirst("\\.s", "");
		String datasetURI = URIprefix + stringToHash(datasetName + "-dataset");
		Resource datasetResource = model.createResource(datasetURI).addProperty(RDFS.label, datasetName + "_dataset")
				.addProperty(RDF.type, DM_dataset);

		String task = typeOfTask(schema.getTargetAttributes());
		
		String [] dsetSpecs = {"supervised", "semi-supervised", "online supervised", "online semi-supervised", "unlabeled"};
		
		
		for (String dsetSpec : dsetSpecs) {
			String dsetLabel = "dset:" + datasetName + "-" + task + "-" + dsetSpec;
			String dsetResourceURI = URIprefix + stringToHash(dsetLabel);
			Resource dsetResource = model.createResource(dsetResourceURI)
					.addProperty(RDFS.label, dsetLabel)
					.addProperty(RDF.type, datasetResource)
					.addProperty(numberOfInstances, Integer.toString(data.getNbRows()))
					.addProperty(nameDataset, datasetName );
			
			
			
			JSONObject datasetSpecObject = (JSONObject)((JSONObject)(((JSONObject)json.get(task)).get(dsetSpec))).get("dataset specification");
			String dsLabel = "ds:" + datasetName + "-" + (String)datasetSpecObject.get("label");
			String dsURI = URIprefix + stringToHash(dsLabel);
			Resource ontoDSResource = model.createResource((String)datasetSpecObject.get("URI")).addProperty(RDFS.label, (String)datasetSpecObject.get("label"));
			Resource dsResource = model.createResource(dsURI)
					.addProperty(is_about, dsetResource)
					.addProperty(RDFS.label, dsLabel)
					.addProperty(RDF.type, ontoDSResource);
			
			JSONObject datatypeObject = (JSONObject)datasetSpecObject.get("datatype");
			String extentionLabel = datasetName + "-" + task;
			if(hasMissing){
				datatypeObject = (JSONObject)datatypeObject.get("with missing");
				extentionLabel =  extentionLabel + "-with missing-"+dsetSpec;
			}
			else{
				datatypeObject = (JSONObject)datatypeObject.get("without missing");
				extentionLabel =  extentionLabel + "-without missing-"+dsetSpec;
			}
			
			String dTypeLabel = "dType:" + datasetName + "-" + (String)datatypeObject.get("label");
			String dTypeURI =  URIprefix + stringToHash(dTypeLabel);
			Resource ontoDTResource = model.createResource((String) datatypeObject.get("URI"))
					.addProperty(RDFS.label, (String) datatypeObject.get("label"));
			Resource dTypeResource = model.createResource(dTypeURI)
					.addProperty(RDF.type, ontoDTResource)
					.addProperty(RDFS.label, dTypeLabel);
			dsResource.addProperty(hasPart, dTypeResource);
			
			
			JSONObject taskObject = (JSONObject)json.get(task);
			JSONObject modeObject = (JSONObject)taskObject.get(dsetSpec);
			String ntaskLabel = "task:" + datasetName + "-" + (String)modeObject.get("label");
			String ntaskURI =  URIprefix + stringToHash(ntaskLabel);
			Resource ontotaskResource = model.createResource((String) modeObject.get("URI"))
					.addProperty(RDFS.label, (String) modeObject.get("label"));
			Resource taskResource = model.createResource(ntaskURI)
					.addProperty(RDFS.label, ntaskLabel)
					.addProperty(RDF.type, ontotaskResource);
			taskResource.addProperty(hasPart, dTypeResource);
			

			
			if(dsetSpec=="online supervised" || dsetSpec== "online semi-supervised"){
				JSONObject baseDTObject = (JSONObject)datatypeObject.get("has_base_datatype");
				String baseLabel = "base_datatype"+ extentionLabel +"|"+(String)baseDTObject.get("label");
				String baseURI = URIprefix + stringToHash(baseLabel);
				Resource ontoBaseResource = model.createResource((String)baseDTObject.get("URI")).addProperty(RDFS.label, (String)baseDTObject.get("label"));
				Resource baseResource = model.createResource(baseURI)
						.addProperty(RDFS.label, baseLabel)
						.addProperty(RDF.type, ontoBaseResource);
				dTypeResource.addProperty(hasBaseDatatype, baseResource);
				
				JSONObject baseDTRoleObject = (JSONObject)baseDTObject.get("is_datatype_role_of");
				String baseRoleLabel = "Dtype"+ extentionLabel +"|"+(String)baseDTRoleObject.get("label");
				String baseRoleURI = URIprefix + stringToHash(baseRoleLabel);
				Resource ontoBaseDTResource = model.createResource((String)baseDTRoleObject.get("URI")).addProperty(RDFS.label, (String)baseDTRoleObject.get("label"));
				Resource baseRoleResource = model.createResource( baseRoleURI)
						.addProperty(RDFS.label, baseRoleLabel)
						.addProperty(RDF.type, ontoBaseDTResource);
				baseResource.addProperty(datatypeRoleOf, baseRoleResource);
				dTypeResource = baseRoleResource;
				datatypeObject = baseDTRoleObject;
			}

			JSONObject descriptiveFCObject = (JSONObject) datatypeObject.get("descriptive FC");	
			JSONObject descritiveDTObject  =  (JSONObject) descriptiveFCObject.get("is_datatype_role_of");
			
			//add descriptive FC to dTypeResource
			String [] descriptiveArrName = new String [1];
			Resource [] comResource = new Resource [1];
			String descDTypeLabel = "descriptiveDtype:";
			descDTypeLabel= descDTypeLabel +extentionLabel;
			String descDTypeURI = URIprefix + stringToHash(descDTypeLabel);
			Resource ontoDescDTResource = model.createResource((String)descritiveDTObject.get("URI"))
					.addProperty(RDFS.label, (String)descritiveDTObject.get("label"));
			Resource descDTypeResource = model.createResource(descDTypeURI)
					.addProperty(RDFS.label, descDTypeLabel)
					.addProperty(RDF.type, ontoDescDTResource);
			comResource[0]=descDTypeResource;
			descriptiveArrName[0]="descriptive";
			Resource ontoDescFC = model.createResource((String) descriptiveFCObject.get("URI"))
					.addProperty(RDFS.label, (String) descriptiveFCObject.get("label"));
			recordOfComplex(dTypeResource, comResource, descriptiveArrName, datasetName+"-"+task+"-"+dsetSpec+(String) descriptiveFCObject.get("label"), ontoDescFC);
			
			// annotate descriptive attributes
			ClusAttrType [] descriptiveAttributes = schema.getDescriptiveAttributes();
			Resource [] descriptiveAttributesResources = new Resource [schema.getDescriptiveAttributes().length];
			String [] descriptiveNames = new String [descriptiveAttributesResources.length];
			for (int i =0; i<descriptiveAttributes.length; i++){
				descriptiveNames[i]=descriptiveAttributes[i].getName();
			}
			for (int i = 0; i<descriptiveAttributes.length; i++) {
				String attrName = descriptiveAttributes[i].getName();
				String attrType = descriptiveAttributes[i].getTypeName();
				String descDtypeAttType = "descriptiveAttribute" + attrName + "DataType"+extentionLabel;
				String descDtypeAttTypeURI = URIprefix + stringToHash(descDtypeAttType);
				Resource descDtypeAttTypeResource = model.createResource(descDtypeAttTypeURI);
				if (attrType.equals("Numeric")) {
					descDtypeAttTypeResource.addProperty(RDF.type, realDatatype)
					.addProperty(RDFS.label,  attrName+" Numeric Attribute:"+extentionLabel);
				} else
				// should I have boolean datatype?
				if (attrType.equals("Nominal")) {
					NominalAttrType nom = (NominalAttrType) descriptiveAttributes[i];
					String value = nom.getTypeString();
					if (value.equals("{0,1}") || value.equals("{1,0}")) {
						// boolean datatype
						descDtypeAttTypeResource.addProperty(RDF.type, booleanDatatype)
						.addProperty(RDFS.label,  attrName+" Binary Attribute:"+extentionLabel);
					} else {
						// discrete datatype
						String[] components = getComponents(value);
						descDtypeAttTypeResource.addProperty(RDF.type, discreteDatatype)
						.addProperty(RDFS.label,  attrName+" Discrete Attribute:"+extentionLabel);
						discreteDatatype(descDtypeAttTypeResource,  extentionLabel,  attrName, components);
					}
				}
				descriptiveAttributesResources[i] = descDtypeAttTypeResource;
			}
			recordOfComplex(descDTypeResource, descriptiveAttributesResources, descriptiveNames, extentionLabel, fieldComponent);
			
			if(dsetSpec=="unlabeled") continue;
			// target
			ClusAttrType [] targets = schema.getTargetAttributes();
			String [] targetNames = new String [targets.length];
			for (int i =0; i<targets.length; i++){
				targetNames[i]=targets[i].getName();
			}
			
			JSONObject targetFCObject = (JSONObject) datatypeObject.get("target FC");
			JSONObject targetDTObject  =  (JSONObject) targetFCObject.get("is_datatype_role_of");
			//add target FC to dTypeResource
			String [] targetArr = new String [1];
			Resource [] targetComResource = new Resource [1];
			String targetDTypeLabel = "targetDtype:"+(String)targetDTObject.get("label")+" | "+extentionLabel;
			String targetDTypeURI = URIprefix + stringToHash(targetDTypeLabel);
			Resource ontoTargetDT = model.createResource((String)targetDTObject.get("URI"))
					.addProperty(RDFS.label, (String)targetDTObject.get("label"));
			Resource targDtypeResource = model.createResource(targetDTypeURI)
					.addProperty(RDF.type, ontoTargetDT)
					.addProperty(RDFS.label, targetDTypeLabel);
			targetComResource[0]=targDtypeResource;
			targetArr[0]="target";
			Resource ontoTargetFCResource = model.createResource((String) targetFCObject.get("URI"))
					.addProperty(RDFS.label, (String) targetFCObject.get("label"));
			recordOfComplex(dTypeResource, targetComResource, targetArr, extentionLabel, ontoTargetFCResource); 
			targDtypeResource = targetComResource[0];
			
			if(targetDTObject.get("has_field_component")!=null){
				JSONObject FCObject = (JSONObject)targetDTObject.get("has_field_component");
				JSONObject FCDataType = (JSONObject)FCObject.get("is_datatype_role_of");
				for (int i =0; i<targets.length; i++) {
					String targetName = targetNames[i];					
					String targetAttributeFCLabel = "targetAttribute-" + targetName + "FC-"+(String)FCObject.get("label")+" | "+extentionLabel;
					String targetAttributeFCURI =  URIprefix + stringToHash(targetAttributeFCLabel);
					Resource ontoFCResource = model.createResource( (String)FCObject.get("URI"))
							.addProperty(RDFS.label,  (String)FCObject.get("label"));
					Resource targetAttributeFCResource = model.createResource(targetAttributeFCURI)
							.addProperty(RDFS.label, targetAttributeFCLabel)
							.addProperty(RDF.type, ontoFCResource);
					targDtypeResource.addProperty(hasFieldComponent, targetAttributeFCResource);
					
					String targetAttributeIDLabel = "targetAttribute-" + targetName + "ID-"+(String)FCObject.get("label")+" | "+extentionLabel;
					String targetAttributeIDURI =  URIprefix + stringToHash(targetAttributeIDLabel);
					Resource targetAttributeIDResource = model.createResource(targetAttributeIDURI)
							.addProperty(RDFS.label, targetAttributeIDLabel)
							.addProperty(RDF.type, fieldIdentifier);
					targetAttributeFCResource.addProperty(hasIdentifier, targetAttributeIDResource);
					
					String targetAttributeDtypeLabel = "targetAttribute-" + targetName + "Dtype-"+(String)FCDataType.get("label")+" | "+extentionLabel;
					String targetAttributeDtypeURI = URIprefix + stringToHash(targetAttributeDtypeLabel);
					Resource ontoFCDTResource = model.createResource((String)FCDataType.get("URI"))
							.addProperty(RDFS.label, (String)FCDataType.get("label"));
					Resource targetAttributeDtypeResource = model.createResource(targetAttributeDtypeURI)
							.addProperty(RDFS.label, targetAttributeDtypeLabel)
							.addProperty(RDF.type, ontoFCDTResource);
					targetAttributeFCResource.addProperty(datatypeRoleOf, targetAttributeDtypeResource);
					
					if(dsetSpec == "semi-supervised" || dsetSpec == "online semi-supervised"){
						
						JSONObject alternativeComponents = (JSONObject) FCDataType.get("has_alternative_component");
						JSONObject alternativeVoidComponents = (JSONObject) alternativeComponents.get("void");
						JSONObject alternativeNonVoidComponents = (JSONObject) alternativeComponents.get("non-void");

						String voidComponentLabel = "targetDtypeAC:"+(String)alternativeVoidComponents.get("label")+" | " + extentionLabel;
						String voidComponentURI = URIprefix + stringToHash(voidComponentLabel);
						Resource ontoAVCResource = model.createResource((String)alternativeVoidComponents.get("URI"))
								.addProperty(RDFS.label, (String)alternativeVoidComponents.get("label"));
						Resource voidComponentResource = model.createResource(voidComponentURI)
								.addProperty(RDFS.label, voidComponentLabel)
								.addProperty(RDF.type, ontoAVCResource);
						targetAttributeDtypeResource.addProperty(hasAlternativeComponent, voidComponentResource);
						
						JSONObject voidDatatypeObject = (JSONObject)alternativeVoidComponents.get("is_datatype_role_of");
						String voidDatatypeLabel = "Alternative Component Datatype: " +  voidDatatypeObject.get("label")+" | " + extentionLabel;
						String voidDatatypeURI = URIprefix + stringToHash(voidDatatypeLabel);
						Resource ontoVDTResource = model.createResource((String) voidDatatypeObject.get("URI"))
								.addProperty(RDFS.label, (String) voidDatatypeObject.get("label"));
						Resource voidDatatypeResource = model.createResource(voidDatatypeURI)
								.addProperty(RDFS.label, voidDatatypeLabel)
								.addProperty(RDF.type, ontoVDTResource);
						voidComponentResource.addProperty(datatypeRoleOf, voidDatatypeResource);
						
						String nonVoidComponentLabel = "targetDtypeAC:"+(String)alternativeNonVoidComponents.get("label")+" | " + extentionLabel;
						String nonVoidComponentURI = URIprefix + stringToHash(nonVoidComponentLabel);
						Resource ontoANVCResource = model.createResource((String)alternativeNonVoidComponents.get("URI"))
								.addProperty(RDFS.label, (String)alternativeNonVoidComponents.get("label"));
						Resource nonVoidComponentResource = model.createResource(nonVoidComponentURI)
								.addProperty(RDFS.label, nonVoidComponentLabel)
								.addProperty(RDF.type, ontoANVCResource);
						targetAttributeDtypeResource.addProperty(hasAlternativeComponent, nonVoidComponentResource);
						
						JSONObject nonVoidDatatypeObject = (JSONObject)alternativeNonVoidComponents.get("is_datatype_role_of");
						String nonVoidDatatypeLabel = "Alternative Component Datatype: " +  nonVoidDatatypeObject.get("label")+" | " + extentionLabel;
						String nonVoidDatatypeURI = URIprefix + stringToHash(nonVoidDatatypeLabel);
						Resource ontoNVDTResource = model.createResource((String) nonVoidDatatypeObject.get("URI"))
								.addProperty(RDFS.label, (String) nonVoidDatatypeObject.get("label"));
						Resource nonVoidDatatypeResource = model.createResource(nonVoidDatatypeURI)
								.addProperty(RDFS.label, nonVoidDatatypeLabel)
								.addProperty(RDF.type, ontoNVDTResource);
						nonVoidComponentResource.addProperty(datatypeRoleOf, nonVoidDatatypeResource);
						targetAttributeDtypeResource = nonVoidDatatypeResource;
						
					}
					if(task == "MTMC"){
						ClusAttrType target = targets[i];
						String [] discreteComponents = getDiscreteComponentsForAttribute(target);
						discreteDatatype(targetAttributeDtypeResource, extentionLabel, target.getName(), discreteComponents);
					}
					
					
				}
				
			}
			else{
				if(dsetSpec == "semi-supervised" || dsetSpec == "online semi-supervised"){
					JSONObject alternativeComponents = (JSONObject) targetDTObject.get("has_alternative_component");
					JSONObject alternativeVoidComponents = (JSONObject) alternativeComponents.get("void");
					JSONObject alternativeNonVoidComponents = (JSONObject) alternativeComponents.get("non-void");
	
					String voidComponentLabel = "targetDtypeAC:"+(String)alternativeVoidComponents.get("label")+" | " + extentionLabel;
					String voidComponentURI = URIprefix + stringToHash(voidComponentLabel);
					Resource onAVCResource = model.createResource((String)alternativeVoidComponents.get("URI"))
							.addProperty(RDFS.label, (String)alternativeVoidComponents.get("label"));
					Resource voidComponentResource = model.createResource(voidComponentURI)
							.addProperty(RDFS.label, voidComponentLabel)
							.addProperty(RDF.type, onAVCResource);
					targDtypeResource.addProperty(hasAlternativeComponent, voidComponentResource);
					
					JSONObject voidDatatypeObject = (JSONObject)alternativeVoidComponents.get("is_datatype_role_of");
					String voidDatatypeLabel = "Alternative Component Datatype: " +  voidDatatypeObject.get("label")+" | " + extentionLabel;
					String voidDatatypeURI = URIprefix + stringToHash(voidDatatypeLabel);
					Resource onVDTResource = model.createResource((String) voidDatatypeObject.get("URI"))
							.addProperty(RDFS.label, (String) voidDatatypeObject.get("label"));
					Resource voidDatatypeResource = model.createResource(voidDatatypeURI)
							.addProperty(RDFS.label, voidDatatypeLabel)
							.addProperty(RDF.type, onVDTResource);
					voidComponentResource.addProperty(datatypeRoleOf, voidDatatypeResource);
					
					String nonVoidComponentLabel = "targetDtypeAC:"+(String)alternativeNonVoidComponents.get("label")+" | " + extentionLabel;
					String nonVoidComponentURI = URIprefix + stringToHash(nonVoidComponentLabel);
					Resource onANVCResource = model.createResource((String)alternativeNonVoidComponents.get("URI"))
							.addProperty(RDFS.label, (String)alternativeNonVoidComponents.get("label"));
					Resource nonVoidComponentResource = model.createResource(nonVoidComponentURI)
							.addProperty(RDFS.label, nonVoidComponentLabel)
							.addProperty(RDF.type, onANVCResource);
					targDtypeResource.addProperty(hasAlternativeComponent, nonVoidComponentResource);
					
					JSONObject nonVoidDatatypeObject = (JSONObject)alternativeNonVoidComponents.get("is_datatype_role_of");
					String nonVoidDatatypeLabel = "Alternative Component Datatype: " +  nonVoidDatatypeObject.get("label")+" | " + extentionLabel;
					String nonVoidDatatypeURI = URIprefix + stringToHash(nonVoidDatatypeLabel);
					Resource onNVDTResource = model.createResource((String) nonVoidDatatypeObject.get("URI"))
							.addProperty(RDFS.label, (String) nonVoidDatatypeObject.get("label"));
					Resource nonVoidDatatypeResource = model.createResource(nonVoidDatatypeURI)
							.addProperty(RDFS.label, nonVoidDatatypeLabel)
							.addProperty(RDF.type, onNVDTResource);
					nonVoidComponentResource.addProperty(datatypeRoleOf, nonVoidDatatypeResource);
					targDtypeResource = nonVoidDatatypeResource;				
				}
			}
			//targDtypeResource instance_of PODATOCEN TIP
			task= typeOfTask(schema.getTargetAttributes());
			switch (task) {
			case "R": {
				break;
			}
			case "BC": {
				break;
			}
			case "MCC": {
				//instance_of discrete datatype
				ClusAttrType target = targets[0];
				String [] discreteComponents = getDiscreteComponentsForAttribute(target);
				discreteDatatype(targDtypeResource, extentionLabel, target.getName(), discreteComponents);
				break;
			}
			
			case "MLC": {
				//first annotate for MLC
				//instanc_of set of discrete
				String discLabel = "target" + "-Discrete-" + extentionLabel;
				String discURI=URIprefix + stringToHash(discLabel);
				Resource discreteResource = model.createResource(discURI)
						.addProperty(RDFS.label, discLabel)
						.addProperty(RDF.type, discreteDatatype);
				discreteDatatype(discreteResource, extentionLabel, "target", targetNames);
				targDtypeResource.addProperty(hasBaseDatatype, discreteResource);
				
				
				break;
			}
			case "MTMCC": {
				break;
			}
			case "MTC": {
				break;
			}
			
			case "MTR": {		
				break;
			}

			default:
				break;
			}		

//			PrintStream bw = new PrintStream("C:/TDB2/AnnotationsCar.rdf");
//			RDFDataMgr.write(bw, model, RDFFormat.RDFXML);
//			break;
		}			
		
	}

	public static String[] getComponents(String value) {
		value = value.replace("{", "");
		value = value.replace("}", "");
		value = value.trim();
		String[] components = value.split(",");
		return components;
	}

	public static void printAllTarget(ClusAttrType[] targetAttributes) {
		System.out.println("number of target attr is " + targetAttributes.length);
		for (ClusAttrType clusAttrType : targetAttributes) {
			System.out.println(clusAttrType.getName() + " " + clusAttrType.getTypeName());
			System.out.println(clusAttrType.getName());
		}
		System.out.println();
	}

	public static String  typeOfTask(ClusAttrType[] targetAttributes) {
		boolean allReals = true;
		for (ClusAttrType clusAttrType : targetAttributes) {
			if (!clusAttrType.getTypeName().equals("Numeric")) {
				allReals = false;
				break;
			}
		}
		if (allReals && targetAttributes.length > 1) {
			return "MTR";
		}
		if (allReals && targetAttributes.length == 1) {
			return "R";
		}
		boolean allbinary = true;
		for (ClusAttrType clusAttrType : targetAttributes) {
			if (!clusAttrType.getTypeName().equals("Nominal")) {
				allbinary = false;
				break;
			}
			if (clusAttrType.getTypeName().equals("Nominal")) {
				NominalAttrType nom = (NominalAttrType) clusAttrType;
				if (!nom.getTypeString().equals("{0,1}") && !nom.getTypeString().equals("{1,0}")) {
					allbinary = false;
					break;
				}
			}
		}
		if (allbinary && targetAttributes.length > 1) {
			return "MLC";
		}
		if (allbinary && targetAttributes.length == 1) {
			return "BC";
		}

		boolean mtc = true;
		for (ClusAttrType clusAttrType : targetAttributes) {
			if (!clusAttrType.getTypeName().equals("Nominal")) {
				mtc = false;
				break;
			}
			if (clusAttrType.getTypeName().equals("Nominal")) {
				NominalAttrType nom = (NominalAttrType) clusAttrType;
				if (nom.getTypeString().equals("{0,1}") || nom.getTypeString().equals("{1,0}")) {
					mtc = false;
					break;
				}
			}
		}
		if (mtc && targetAttributes.length > 1) {
			return "MTMCC";
		}
		if (mtc && targetAttributes.length == 1) {
			return "MCC";
		}
		if(!mtc && !allbinary && targetAttributes.length>1){
			return "MTC";
		}
		return "other";
	}
	
	public static void createRDFAll(JSONObject jsonObject) throws IOException, ClusException{
		String loc= "C:/Users/Ana/Desktop/Clus3/datasets";
		File folder = new File(loc);
		File[] listOfFiles = folder.listFiles();
		for (File file : listOfFiles) {
			if(file.isFile()&&file.getName().endsWith(".s")){
				String[] settingsP = new String[1];
				settingsP[0] = file.getName();
				String [] parts = file.getName().split("\\.s");
				createDatasetAnnotations(settingsP, "C:/TDB2", parts[0]+".rdf", jsonObject);
				
			}
		}
	}
	
	public static void main(String[] args) throws IOException, ClusException {
		addPropertyLabels();
		String filePath="C:/Users/Ana/Desktop/Clus3/DataJson.json";
		try {
			FileReader reader = new FileReader(filePath);
			JSONParser jsonParser = new JSONParser();
			JSONObject jsonObject = (JSONObject) jsonParser.parse(reader);
			createRDFAll(jsonObject);
			PrintStream bw = new PrintStream("C:/BookChapter/Annotations.rdf");
			RDFDataMgr.write(bw, model, RDFFormat.RDFXML);
			System.out.println("final");
		} catch (FileNotFoundException ex) {
			ex.printStackTrace();
		} catch (IOException ex) {
			ex.printStackTrace();
		} catch (ParseException ex) {
			ex.printStackTrace();
		} catch (NullPointerException ex) {
			ex.printStackTrace();
		}

	}
}