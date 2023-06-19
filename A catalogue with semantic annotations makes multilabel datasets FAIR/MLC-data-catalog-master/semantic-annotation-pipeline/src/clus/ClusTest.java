package clus;

import java.io.FileReader;
import java.io.IOException;
import org.json.simple.JSONObject;
import org.json.simple.parser.JSONParser;
import org.json.simple.parser.ParseException;

import com.google.gson.JsonArray;
import com.google.gson.JsonElement;
import com.google.gson.JsonObject;
import com.google.gson.JsonParser;

import java.io.File;
import java.io.PrintStream;
import java.io.UnsupportedEncodingException;
import java.security.MessageDigest;
import java.security.NoSuchAlgorithmException;
import java.util.ArrayList;
import java.util.LinkedHashMap;
import java.util.Map;

//import org.apache.commons.math.stat.descriptive.rank.Percentile;
//import org.apache.commons.math.stat.descriptive.rank.Median;
import org.apache.commons.math3.stat.descriptive.DescriptiveStatistics;
import org.apache.jena.ontology.OntModel;
import org.apache.jena.ontology.OntModelSpec;
import org.apache.jena.ontology.OntProperty;
import org.apache.jena.rdf.model.*;
import org.apache.jena.vocabulary.*;
import javax.xml.bind.DatatypeConverter;
import org.apache.jena.riot.RDFDataMgr;
import org.apache.jena.riot.RDFFormat;
import clus.data.rows.RowData;
import clus.data.type.ClusAttrType;
import clus.data.type.ClusSchema;
import clus.data.type.NominalAttrType;
import clus.data.type.NumericAttrType;
import clus.ext.hierarchical.ClassTerm;
import clus.ext.hierarchical.ClassesAttrType;
import clus.jeans.util.cmdline.CMDLineArgs;
import clus.jeans.util.cmdline.CMDLineArgsProvider;
import clus.main.Settings;
import clus.util.ClusException;

public class ClusTest implements CMDLineArgsProvider {
	public static String URIprefix = "http://ontodm.com/SemanticAnnotation#";
	public static Model model = ModelFactory.createDefaultModel();
	public static String hierarchy = "";
	public static JsonArray ontologyJsonArray;
	public static Resource DM_dataset = model.createResource("http://www.ontodm.com/OntoDM-core/OntoDM_000144");
	public static Resource recordDatatype = model.createResource("http://ontodm.com/OntoDT#OntoDT_950419");
	// .addProperty(RDFS.label, "record (tuple) datatype");
	public static Resource targetFC = model.createResource("http://www.ontodm.com/OntoDT#OntoDT_0000397");
	// .addProperty(RDFS.label, "target field component");
	public static Resource fieldIdentifier = model.createResource("http://ontodm.com/OntoDT#OntoDT_inst_507131");
	// .addProperty(RDFS.label, "field identifier");
	public static Resource recordOfPrimitiveDatatype = model.createResource("http://ontodm.com/OntoDT#OntoDT_521859");
	// .addProperty(RDFS.label, "record of primitives datatype");
	public static Resource fieldComponent = model.createResource("http://ontodm.com/OntoDT#OntoDT_059114");
	// .addProperty(RDFS.label, "field component");
	public static Resource discreteDatatype = model.createResource("http://ontodm.com/OntoDT#OntoDT_608148");
	// .addProperty(RDFS.label, "discrete datatype");
	public static Resource discreteValueList = model.createResource("http://ontodm.com/OntoDT#OntoDT_089686");
	// .addProperty(RDFS.label, "discrete value list");
	public static Resource discreteValueIdentifier = model.createResource("http://ontodm.com/OntoDT#OntoDT_467794");
	// .addProperty(RDFS.label, "discrete value identifier");
	public static Resource realDatatype = model.createResource("http://ontodm.com/OntoDT#OntoDT_150012");
	// .addProperty(RDFS.label, "real datatype");
	public static Resource booleanDatatype = model.createResource("http://www.ontodm.com/OntoDT#OntoDT_0000002");
	// .addProperty(RDFS.label, "boolean datatype");
	public static Resource setOfDiscreteDatatype = model.createResource("http://ontodm.com/OntoDT#OntoDT_377271");
	// .addProperty(RDFS.label, "set of discrete");
	public static Resource discreteBaseType = model.createResource("http://ontodm.com/OntoDT#OntoDT_339518");
	// .addProperty(RDFS.label, "discrete base type");
	public static Resource recordOfBooleanDatatype = model.createResource("http://ontodm.com/OntoDT#OntoDT_360708");
	// .addProperty(RDFS.label, "record of boolean");
	public static Resource recordOfRealDatatype = model.createResource("http://ontodm.com/OntoDT#OntoDT_471356");
	// .addProperty(RDFS.label, "record of real datatype");
	public static Resource recordOfDiscreteDatatype = model.createResource("http://ontodm.com/OntoDT#OntoDT_595741");
	// .addProperty(RDFS.label, "record of discrete ");
	public static Resource namedTreeNodeComponent = model
			.createResource("http://www.ontodm.com/OntoDT#OntoDT_ca96378e_c421_454c_9ba6_db5010ce068a");
	

	public static OntProperty is_about;
	public static OntProperty hasMember;
	public static OntProperty hasIdentifier;
	public static OntProperty datatypeRoleOf;
	public static OntProperty numberOfInstances;
	public static OntProperty nameDataset;
	public static OntProperty hasFieldComponent;
	public static OntProperty hasPart;
	public static OntProperty hasBaseDatatype;
	public static OntProperty hasAlternativeComponent;
	public static OntProperty numTargets;
	public static OntProperty numDescriptiveFeatures;
	public static OntProperty hasMissingValues;
	public static OntProperty hasNodeComponent;
	public static OntProperty nodeLabel;
	public static OntProperty hasTestSet;
	public static OntProperty featureName;
	public static OntProperty featureType;
	public static OntProperty featureCharacteristics;
	public static OntProperty hasName;

	static {
		OntModel ontModel = ModelFactory.createOntologyModel(OntModelSpec.OWL_DL_MEM);
		is_about = ontModel.createObjectProperty("http://purl.obolibrary.org/obo/IAO_0000136");
		hasMember = ontModel.createObjectProperty("http://semanticscience.org/resource/SIO_000059");
		hasIdentifier = ontModel.createObjectProperty("http://semanticscience.org/resource/SIO_000671");
		datatypeRoleOf = ontModel.createObjectProperty("http://ontodm.com/OntoDT#OntoDT_0000010");
		numberOfInstances = ontModel.createDatatypeProperty(URIprefix + "numberOfInstances");
		nameDataset = ontModel.createAnnotationProperty(URIprefix + "nameDataset");
		hasFieldComponent = ontModel.createObjectProperty("http://www.ontodm.com/OntoDT/OntoDT_80000000");
		hasPart = ontModel.createObjectProperty("http://www.obofoundry.org/ro/ro.owl#has_part");
		hasBaseDatatype = ontModel.createObjectProperty("http://www.ontodm.com/OntoDT/OntoDT_80000004");
		hasAlternativeComponent = ontModel.createObjectProperty("http://www.ontodm.com/OntoDT/OntoDT_80000001");
		numTargets = ontModel.createDatatypeProperty(URIprefix + "numOfTargets");
		numDescriptiveFeatures = ontModel.createDatatypeProperty(URIprefix + "numOfDescriptiveFeatures");
		hasMissingValues = ontModel.createDatatypeProperty(URIprefix + "hasMissingValues");
		hasNodeComponent = ontModel.createObjectProperty("http://www.ontodm.com/OntoDT/OntoDT_80000003");
		nodeLabel = ontModel.createDatatypeProperty(URIprefix + "nodeLabel");
		hasTestSet = ontModel.createDatatypeProperty(URIprefix + "hasTestDataset");
		featureName = ontModel.createDatatypeProperty(URIprefix + "featureName");
		featureType = ontModel.createDatatypeProperty(URIprefix + "featureType");
		featureCharacteristics = ontModel.createDatatypeProperty(URIprefix + "featureCharacteristics");
		hasName = ontModel.createDatatypeProperty("http://www.ontodm.com/OntoDM-core/OntoDM_000074");
		model.add(ontModel);

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
	
	public static String findURI(JsonArray ja, String label) {
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
	
	public static String findLabel(JsonArray ja, String URI) {
		try {
			for (JsonElement jsonElement : ja) {
				JsonObject jo = (JsonObject) jsonElement;
				JsonElement idJson = jo.get("@id");						
				String id = idJson.toString().replace("\"", "");
				if(id.equals(URI)) {
					JsonArray deprecatedJsonArr = (JsonArray) jo.get("http://purl.obolibrary.org/obo/IAO_0100001");
					if(deprecatedJsonArr!=null &&deprecatedJsonArr.get(0)!=null) {
						JsonObject deprecatedJson = (JsonObject) deprecatedJsonArr.get(0);
						return findLabel(ja, deprecatedJson.get("@id").getAsString());
					}
					else {
						JsonArray labelArray = (JsonArray) jo.get("http://www.w3.org/2000/01/rdf-schema#label");
						if (labelArray != null) {
							JsonObject labelJson = (JsonObject) labelArray.get(0);
							if (labelJson != null) {
								String labelValue = labelJson.get("@value").toString().replace("\"", "");
								if (labelValue != null) {

									return labelValue;
								}
							}
						}
						
					}
				}
			
			}
		}
		catch (Exception e) {
			return "GO:"+URI.split("GO_")[1];
		}
		return "";
		
	
	}

	static Resource createResource(Resource type, String label) {
		Resource newResource = model.createResource(URIprefix + stringToHash(label));
		if (type != null) {
			newResource.addProperty(RDF.type, type);
		}
		if (label != null) {
			newResource.addProperty(RDFS.label, label);
		}
		return newResource;
	}

	public static String stringToHash(String name) {
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

	public static void discreteDatatype(Resource resourceDiscreteDatatype, String spec, String attrName,
			String[] components) {
		String DiscreteListLabel = attrName + "-dis-list:" + spec;
		// descDtypeAttDisList instance_of discrete-value-list
		Resource DisListResource = createResource(discreteValueList, DiscreteListLabel);

		// descDtypeAttType has_member descDtypeAttDisList
		resourceDiscreteDatatype.addProperty(hasMember, DisListResource);
		for (int i = 0; i < components.length; i++) {
			String component = components[i];
			int num = i + 1;
			String AttComponent = attrName + "DiscreteValueIdentifier" + num + ":" + spec;
			String AttComponentURI = URIprefix + stringToHash(AttComponent);
			// AttComponent instance_of discrete value identifier
			Resource AttComponentResource = model.createResource(AttComponentURI)
					.addProperty(RDFS.label, spec + "|" + attrName + ":" + component)
					.addProperty(RDF.type, discreteValueIdentifier);
			// descDtypeAttDisList has-member AttComponent
			DisListResource.addProperty(hasMember, AttComponentResource);
		}

	}

	public static void recordOfComplex(Resource recordResource, Resource[] complexResources, String[] components,
			String extention, Resource FC) {
		// We can use this function for record of real, record of primitives, record of
		// boolean..
		for (int i = 0; i < components.length; i++) {
			String fieldComponentLabel = components[i] + "FC:" + extention;
			Resource fieldComponentResource = createResource(FC, fieldComponentLabel);
			recordResource.addProperty(hasFieldComponent, fieldComponentResource);

			String fieldIDLabel = components[i] + "ID:" + extention;
			Resource fieldIDResource = createResource(fieldIdentifier, fieldIDLabel);
			fieldComponentResource.addProperty(hasIdentifier, fieldIDResource);
			fieldComponentResource.addProperty(datatypeRoleOf, complexResources[i]);

		}
	}

	public static String[] getDiscreteComponentsForAttribute(ClusAttrType attribute) {
		NominalAttrType nomT = (NominalAttrType) attribute;
		String value = nomT.getTypeString();
		String[] components = getComponents(value);
		return components;
	}

	public static void annotateBaseType(JSONObject baseDTObject, JSONObject baseDTRoleObject,  JSONObject datatypeObject,
			String extentionLabel, Resource dTypeResource) {
		String baseLabel = "base_datatype" + extentionLabel + "|" + (String) baseDTObject.get("label");
		Resource ontoBaseResource = model.createResource((String) baseDTObject.get("URI"));
		Resource baseResource = createResource(ontoBaseResource, baseLabel);
		dTypeResource.addProperty(hasBaseDatatype, baseResource);

		String baseRoleLabel = "Dtype" + extentionLabel + "|" + (String) baseDTRoleObject.get("label");
		Resource ontoBaseDTResource = model.createResource((String) baseDTRoleObject.get("URI"));
		Resource baseRoleResource = createResource(ontoBaseDTResource, baseRoleLabel);
		baseResource.addProperty(datatypeRoleOf, baseRoleResource);
		dTypeResource = baseRoleResource;
		datatypeObject = baseDTRoleObject;
	}

	@SuppressWarnings("unchecked")
	public static void createDatasetAnnotations(String[] args, String tdbLocation, String rdfName, JSONObject json)
			throws IOException, ClusException, java.text.ParseException {
		Clus clus = new Clus();

		CMDLineArgs cargs = new CMDLineArgs(clus);
		Settings sett = clus.getSettings();
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
		Resource datasetResource = createResource(null, datasetName + "_dataset");
		datasetResource.addProperty(RDFS.subClassOf, DM_dataset);

		String task = typeOfTask(schema.getTargetAttributes());
		System.out.println("Task: " + task);
		
		
		ArrayList<ClusAttrType> attributes = new ArrayList<>();

		
//		String[] dsetSpecs = { "supervised", "semi-supervised", "online supervised", "online semi-supervised",
//				"unlabeled", "online unlabeled" };
		String[] dsetSpecs = {"supervised"};

		for (String dsetSpec : dsetSpecs) {
			if (dsetSpec == "online unlabeled" || dsetSpec == "unlabeled")
				task = "U";
			String dsetLabel = "dset:" + datasetName + "-" + task + "-" + dsetSpec;
			Resource dsetResource = createResource(datasetResource, dsetLabel);
			dsetResource.addLiteral(numberOfInstances, data.getNbRows()).addProperty(nameDataset, datasetName)
					.addLiteral(hasMissingValues, hasMissing);

			if (sett.getTestFile() != null) {
				dsetResource.addLiteral(hasTestSet, sett.getTestFile());
			}

			JSONObject datasetSpecObject = (JSONObject) ((JSONObject) (((JSONObject) json.get(task)).get(dsetSpec)))
					.get("dataset specification");
			String dsLabel = "ds:" + datasetName + "-" + (String) datasetSpecObject.get("label") + "-" + dsetSpec;
			Resource ontoDSResource = model.createResource((String) datasetSpecObject.get("URI"));
			Resource dsResource = createResource(ontoDSResource, dsLabel);
			dsResource.addProperty(is_about, dsetResource);

			if (task == "MLC") {
				// annotate data-set with MLC meta-features
				System.out.println("Annotate meta for: " + datasetName);
				MetaFeatures mf = new MetaFeatures(model);
				try {
					mf.metaFeaturesMLC(datasetName, dsetResource, dsetSpec);
				} catch (Exception e) {
					e.printStackTrace();
				}
			}

			JSONObject datatypeObject = (JSONObject) datasetSpecObject.get("datatype");
			String extentionLabel = datasetName + "-" + task;

			String withOrWithoutMissing = hasMissing ? "with missing" : "without missing";
			datatypeObject = (JSONObject) datatypeObject.get(withOrWithoutMissing);
			extentionLabel = extentionLabel + "-" + withOrWithoutMissing + "-" + dsetSpec;

			String dTypeLabel = "dType:" + datasetName + "-" + (String) datatypeObject.get("label");
			Resource ontoDTResource = model.createResource((String) datatypeObject.get("URI"));
			Resource dTypeResource = createResource(ontoDTResource, dTypeLabel);
			dsResource.addProperty(hasPart, dTypeResource);

			JSONObject taskObject = (JSONObject) json.get(task);
			JSONObject modeObject = (JSONObject) taskObject.get(dsetSpec);
			String ntaskLabel = "task:" + datasetName + "-" + (String) modeObject.get("label");
			Resource ontotaskResource = model.createResource((String) modeObject.get("URI"));
			Resource taskResource = createResource(ontotaskResource, ntaskLabel);
			taskResource.addProperty(hasMember, dTypeResource);

			if (dsetSpec == "online supervised" || dsetSpec == "online semi-supervised"
					|| dsetSpec == "online unlabeled") {
				// JSONObject baseDTObject = (JSONObject)
				// datatypeObject.get("has_base_datatype");
				// JSONObject baseDTRoleObject = (JSONObject)
				// baseDTObject.get("is_datatype_role_of");
				// annotateBaseType(baseDTObject, baseDTRoleObject, datatypeObject,
				// extentionLabel, dTypeResource);
				JSONObject baseDTObject = (JSONObject) datatypeObject.get("has_base_datatype");
				String baseLabel = "base_datatype" + extentionLabel + "|" + (String) baseDTObject.get("label");
				String baseURI = URIprefix + stringToHash(baseLabel);
				Resource ontoBaseResource = model.createResource((String) baseDTObject.get("URI"))
						.addProperty(RDFS.label, (String) baseDTObject.get("label"));
				Resource baseResource = model.createResource(baseURI).addProperty(RDFS.label, baseLabel)
						.addProperty(RDF.type, ontoBaseResource);
				dTypeResource.addProperty(hasBaseDatatype, baseResource);

				JSONObject baseDTRoleObject = (JSONObject) baseDTObject.get("is_datatype_role_of");
				String baseRoleLabel = "Dtype" + extentionLabel + "|" + (String) baseDTRoleObject.get("label");
				String baseRoleURI = URIprefix + stringToHash(baseRoleLabel);
				Resource ontoBaseDTResource = model.createResource((String) baseDTRoleObject.get("URI"))
						.addProperty(RDFS.label, (String) baseDTRoleObject.get("label"));
				Resource baseRoleResource = model.createResource(baseRoleURI).addProperty(RDFS.label, baseRoleLabel)
						.addProperty(RDF.type, ontoBaseDTResource);
				baseResource.addProperty(datatypeRoleOf, baseRoleResource);
				dTypeResource = baseRoleResource;
				datatypeObject = baseDTRoleObject;
			}

			JSONObject descriptiveFCObject = (JSONObject) datatypeObject.get("descriptive FC");
			JSONObject descritiveDTObject = (JSONObject) descriptiveFCObject.get("is_datatype_role_of");

			// add descriptive FC to dTypeResource
			String[] descriptiveArrName = new String[1];
			Resource[] comResource = new Resource[1];
			String descDTypeLabel = "descriptiveDtype:";
			descDTypeLabel = descDTypeLabel + extentionLabel;
			Resource ontoDescDTResource = model.createResource((String) descritiveDTObject.get("URI"));
			Resource descDTypeResource = createResource(ontoDescDTResource, descDTypeLabel);
			comResource[0] = descDTypeResource;
			descriptiveArrName[0] = "descriptive";
			Resource ontoDescFC = model.createResource((String) descriptiveFCObject.get("URI"));
			recordOfComplex(dTypeResource, comResource, descriptiveArrName,
					datasetName + "-" + task + "-" + dsetSpec + (String) descriptiveFCObject.get("label"), ontoDescFC);

			// annotate descriptive attributes
			ClusAttrType[] descriptiveAttributes = schema.getDescriptiveAttributes();
			dsetResource.addLiteral(numDescriptiveFeatures, descriptiveAttributes.length);
			Resource[] descriptiveAttributesResources = new Resource[schema.getDescriptiveAttributes().length];
			String[] descriptiveNames = new String[descriptiveAttributesResources.length];
			
		
			for (int i = 0; i < descriptiveAttributes.length; i++) {
				descriptiveNames[i] = descriptiveAttributes[i].getName();
				attributes.add(descriptiveAttributes[i]);
			}			
			
			for (int i = 0; i < descriptiveAttributes.length; i++) {
				String attrName = descriptiveAttributes[i].getName();
				String attrType = descriptiveAttributes[i].getTypeName();

				String descDtypeAttType = "descriptiveAttribute" + attrName + "DataType" + extentionLabel;
				String descDtypeAttTypeURI = URIprefix + stringToHash(descDtypeAttType);
				Resource descDtypeAttTypeResource = model.createResource(descDtypeAttTypeURI);
				descDtypeAttTypeResource.addLiteral(featureName, attrName);
				if (attrType.equals("Numeric")) {
					descDtypeAttTypeResource.addProperty(RDF.type, realDatatype)
							.addProperty(RDFS.label, attrName + " Numeric Attribute:" + extentionLabel)
							.addLiteral(featureType, "numeric");
				} else
				// should I have boolean datatype?
				if (attrType.equals("Nominal")) {
					NominalAttrType nom = (NominalAttrType) descriptiveAttributes[i];
					String value = nom.getTypeString();
					if (value.equals("{0,1}") || value.equals("{1,0}")) {
						// boolean datatype
						descDtypeAttTypeResource.addProperty(RDF.type, booleanDatatype)
								.addProperty(RDFS.label, attrName + " Binary Attribute:" + extentionLabel)
								.addLiteral(featureType, "nominal");
					} else {
						// discrete datatype
						String[] components = getComponents(value);
						descDtypeAttTypeResource.addProperty(RDF.type, discreteDatatype)
								.addProperty(RDFS.label, attrName + " Discrete Attribute:" + extentionLabel)
								.addLiteral(featureType, "nominal");
						discreteDatatype(descDtypeAttTypeResource, extentionLabel, attrName, components);

					}
				}
				///// feature characteristics
				DescriptiveStatistics stats = new DescriptiveStatistics();
				if (attrType.equals("Numeric")) {
					double[] featureVector = new double [data.getNbRows()];
					NumericAttrType at = (NumericAttrType) descriptiveAttributes[i];
					for (int k = 0; k < data.getNbRows(); k++) {
						featureVector[k] = at.getNumeric(data.getData()[k]);
					}
					for (int j = 0; j < featureVector.length; j++) {
						stats.addValue(featureVector[j]);
					}
					descDtypeAttTypeResource.addLiteral(featureCharacteristics, stats.getMin() + ","
							+ stats.getPercentile(25) + "," +stats.getPercentile(25)+","+ stats.getPercentile(50) + ","
							+ stats.getPercentile(75) + ","+ stats.getPercentile(75) + "," + stats.getMax());

				} else if (attrType.equals("Nominal")) {
					int[] featureVector = new int [data.getNbRows()];
					NominalAttrType nominalDescriptiveAttribute = (NominalAttrType) descriptiveAttributes[i];
					for (int k = 0; k < data.getNbRows(); k++) {
						featureVector[k] = nominalDescriptiveAttribute.getNominal(data.getData()[k]);
					}
					
					int labelsArraySize = hasMissing? nominalDescriptiveAttribute.m_Values.length+1:nominalDescriptiveAttribute.m_Values.length;
					String [] labels = new String [labelsArraySize];
					for(int z=0; z<nominalDescriptiveAttribute.m_Values.length; z++) {
						labels[z] = nominalDescriptiveAttribute.m_Values[z];
					}
					if(hasMissing)
						labels[nominalDescriptiveAttribute.m_Values.length] = "missing";
					
					@SuppressWarnings("rawtypes")
					Map<String, Integer> frequency = new LinkedHashMap();
					for(int j = 0; j<labels.length; j++) {
						frequency.put(labels[j], 0);
					}
					for (int j = 0; j < featureVector.length; j++) {
						if (frequency.containsKey(labels[featureVector[j]])) {
							frequency.put(labels[featureVector[j]], frequency.get(labels[featureVector[j]]) + 1);
						}
					}
					String freq = frequency.toString();
					freq = freq.replace("{", "");
					freq = freq.replace("}", "");
//					System.out.println(freq);
					descDtypeAttTypeResource.addLiteral(featureCharacteristics, freq);
				}
				//////// end feature characteristics

				descriptiveAttributesResources[i] = descDtypeAttTypeResource;
			}
			recordOfComplex(descDTypeResource, descriptiveAttributesResources, descriptiveNames, extentionLabel,
					fieldComponent);
			if (dsetSpec == "unlabeled" || dsetSpec == "online unlabeled") {
				dsetResource.addLiteral(numTargets, 0);
				continue;
			}

			// target
			ClusAttrType[] targets = schema.getTargetAttributes();
			dsetResource.addLiteral(numTargets, targets.length);
			String[] targetNames = new String[targets.length];
			for (int i = 0; i < targets.length; i++) {
				targetNames[i] = targets[i].getName();
				attributes.add(targets[i]);
			}


			JSONObject targetFCObject = (JSONObject) datatypeObject.get("target FC");
			JSONObject targetDTObject = (JSONObject) targetFCObject.get("is_datatype_role_of");
			// add target FC to dTypeResource
			String[] targetArr = new String[1];
			Resource[] targetComResource = new Resource[1];
			String targetDTypeLabel = "targetDtype:" + (String) targetDTObject.get("label") + " | " + extentionLabel;
			Resource ontoTargetDT = model.createResource((String) targetDTObject.get("URI")).addProperty(RDFS.label,
					(String) targetDTObject.get("label"));
			Resource targDtypeResource = createResource(ontoTargetDT, targetDTypeLabel);
			targetComResource[0] = targDtypeResource;
			targetArr[0] = "target";
			Resource ontoTargetFCResource = model.createResource((String) targetFCObject.get("URI"))
					.addProperty(RDFS.label, (String) targetFCObject.get("label"));
			recordOfComplex(dTypeResource, targetComResource, targetArr, extentionLabel, ontoTargetFCResource);
			targDtypeResource = targetComResource[0];

			if (targetDTObject.get("has_base_datatype") != null) {
				targetDTObject = (JSONObject) targetDTObject.get("has_base_datatype");
				String baseLabel1 = "base_datatype" + extentionLabel + "|" + (String) targetDTObject.get("label");
				String baseURI1 = URIprefix + stringToHash(baseLabel1);
				Resource ontoBaseResource1 = model.createResource((String) targetDTObject.get("URI"))
						.addProperty(RDFS.label, (String) targetDTObject.get("label"));
				Resource baseResource1 = model.createResource(baseURI1).addProperty(RDFS.label, baseLabel1)
						.addProperty(RDF.type, ontoBaseResource1);
				targDtypeResource.addProperty(hasBaseDatatype, baseResource1);

			}

			if (targetDTObject.get("has_field_component") != null) {
				JSONObject FCObject = (JSONObject) targetDTObject.get("has_field_component");
				JSONObject FCDataType = (JSONObject) FCObject.get("is_datatype_role_of");
				for (int i = 0; i < targets.length; i++) {
					String targetName = targetNames[i];
					String targetAttributeFCLabel = "targetAttribute-" + targetName + "FC-"
							+ (String) FCObject.get("label") + " | " + extentionLabel;
					Resource ontoFCResource = model.createResource((String) FCObject.get("URI"));
					Resource targetAttributeFCResource = createResource(ontoFCResource, targetAttributeFCLabel);
					targDtypeResource.addProperty(hasFieldComponent, targetAttributeFCResource);

					String targetAttributeIDLabel = "targetAttribute-" + targetName + "ID-"
							+ (String) FCObject.get("label") + " | " + extentionLabel;
					Resource targetAttributeIDResource = createResource(fieldIdentifier, targetAttributeIDLabel);
					targetAttributeFCResource.addProperty(hasIdentifier, targetAttributeIDResource);

					String targetAttributeDtypeLabel = "targetAttribute-" + targetName + "Dtype-"
							+ (String) FCDataType.get("label") + " | " + extentionLabel;
					Resource ontoFCDTResource = model.createResource((String) FCDataType.get("URI"));
					Resource targetAttributeDtypeResource = createResource(ontoFCDTResource, targetAttributeDtypeLabel);
					targetAttributeFCResource.addProperty(datatypeRoleOf, targetAttributeDtypeResource);

					if (dsetSpec == "semi-supervised" || dsetSpec == "online semi-supervised") {
						JSONObject alternativeComponents = (JSONObject) FCDataType.get("has_alternative_component");
						JSONObject alternativeVoidComponents = (JSONObject) alternativeComponents.get("void");
						JSONObject alternativeNonVoidComponents = (JSONObject) alternativeComponents.get("non-void");
						@SuppressWarnings("unused")
						Resource voidDatatypeResource = annotateAlternativeComponent(alternativeVoidComponents,
								extentionLabel, targetAttributeDtypeResource, targets, targetNames, task);
						Resource nonVoidDatatypeResource = annotateAlternativeComponent(alternativeNonVoidComponents,
								extentionLabel, targetAttributeDtypeResource, targets, targetNames, task);
						targetAttributeDtypeResource = nonVoidDatatypeResource;
					}
					if (task == "MTMCC") {
						ClusAttrType target = targets[i];
						String[] discreteComponents = getDiscreteComponentsForAttribute(target);
						discreteDatatype(targetAttributeDtypeResource, extentionLabel, target.getName(),
								discreteComponents);
					}

				}

			} else {
				if (dsetSpec == "semi-supervised" || dsetSpec == "online semi-supervised") {
					JSONObject alternativeComponents = (JSONObject) targetDTObject.get("has_alternative_component");
					JSONObject alternativeVoidComponents = (JSONObject) alternativeComponents.get("void");
					JSONObject alternativeNonVoidComponents = (JSONObject) alternativeComponents.get("non-void");
					@SuppressWarnings("unused")
					Resource voidDatatypeResource = annotateAlternativeComponent(alternativeVoidComponents,
							extentionLabel, targDtypeResource, targets, targetNames, task);
					Resource nonVoidDatatypeResource = annotateAlternativeComponent(alternativeNonVoidComponents,
							extentionLabel, targDtypeResource, targets, targetNames, task);
					targDtypeResource = nonVoidDatatypeResource;
				}
			}
			// targDtypeResource instance_of PODATOCEN TIP
			task = typeOfTask(schema.getTargetAttributes());
			switch (task) {
			case "MCC": {
				// instance_of discrete datatype
				ClusAttrType target = targets[0];
				String[] discreteComponents = getDiscreteComponentsForAttribute(target);
				discreteDatatype(targDtypeResource, extentionLabel, target.getName(), discreteComponents);
				break;
			}
			case "MLC": {
				// first annotate for MLC
				// instanc_of set of discrete
				String discLabel = "target" + "-Discrete-" + extentionLabel;
				Resource discreteResource = createResource(discreteDatatype, discLabel);
				discreteDatatype(discreteResource, extentionLabel, "target", targetNames);
				targDtypeResource.addProperty(hasBaseDatatype, discreteResource);
				//annotate feature characteristics for the MLC target 
				
				StringBuilder sb = new StringBuilder();
				for(ClusAttrType target:targets) {
					
					int[] featureVector = new int [data.getNbRows()];
					NominalAttrType nominalTargetAttribute = (NominalAttrType) target;
					for (int k = 0; k < data.getNbRows(); k++) {
						featureVector[k] = nominalTargetAttribute.getNominal(data.getData()[k]);
					}
					
					int labelsArraySize = hasMissing? nominalTargetAttribute.m_Values.length+1:nominalTargetAttribute.m_Values.length;
					String [] labels = new String [labelsArraySize];
					for(int z=0; z<nominalTargetAttribute.m_Values.length; z++) {
						labels[z] = nominalTargetAttribute.m_Values[z];
					}
					if(hasMissing)
						labels[nominalTargetAttribute.m_Values.length] = "missing";
					
					@SuppressWarnings("rawtypes")
					Map<String, Integer> frequency = new LinkedHashMap();
					for(int j = 0; j<labels.length; j++) {
						frequency.put(labels[j], 0);
					}
					for (int j = 0; j < featureVector.length; j++) {
						if (frequency.containsKey(labels[featureVector[j]])) {
							frequency.put(labels[featureVector[j]], frequency.get(labels[featureVector[j]]) + 1);
						}
					}
					
					String freq = frequency.toString();
					freq = freq.replace(" ", "");
					sb.append(target.getName()+":"+freq+";");

				}
				sb.deleteCharAt(sb.length()-1);
				targDtypeResource.addLiteral(featureCharacteristics, sb.toString());
				break;
			}
			case "HMLC-DAG":
			case "HMLC-tree": {
//				ClassesAttrType target = (clus.ext.hierarchical.ClassesAttrType) targets[0];
//				ClassTerm root = target.getHier().getRoot();
//				String rootLabel = "root-" + extentionLabel;
//				Resource rootResource = createResource(namedTreeNodeComponent, rootLabel).addLiteral(nodeLabel, "root");
//				targDtypeResource.addProperty(hasFieldComponent, rootResource);
//				Object obj = new JsonParser().parse(new FileReader("C:\\Users\\ana\\Desktop\\bookChapter\\Clus3\\src\\GO-LD.owl"));
//				JsonArray ontologyLD = (JsonArray) obj;
//				hierarchy = "";
//				annotateTree(root, rootResource, extentionLabel, ontologyLD);
//				System.out.println("hier: ");
//				System.out.println(hierarchy.toString());
				break;
			}

			default:
				break;
			}
			
//			if(datasetName.equals("Forestry_Kras")) {
//				Resource ontoFestureSetSpecificationResource = model.createResource("http://www.ontodm.com/OntoDM-core/OntoDM_000128");
//				Resource ontoFeatureSpecificationResource = model.createResource("http://www.ontodm.com/OntoDM-core/OntoDM_000298");
//				Resource featureSetSpecificationResource = createResource(ontoFestureSetSpecificationResource, datasetName+":"+"featureSetSpecification");
//				dsetResource.addProperty(hasPart, featureSetSpecificationResource);				
//				for (int i = 0; i < attributes.size(); i++) {
//					String attributeName = attributes.get(i).getName();
//					String identifierLabel = attributeName + "ID:" + extentionLabel;
//					Resource identiferResource = createResource(fieldIdentifier, identifierLabel);
//					Resource featureSpecificationResource = createResource(ontoFeatureSpecificationResource, datasetName+":"+attributeName+":featureSpecification")
//							.addProperty(hasIdentifier, identiferResource);
//					featureSetSpecificationResource.addProperty(hasPart, featureSpecificationResource);
//				}	
//				ForestryAnnotations fa = new ForestryAnnotations(model, schema, datasetName);
//				fa.annotateDataset();
//				fa.writeModel();
//			}
			
		}

	}

	public static String annotateGOTerms(ClassTerm root, String nodeLabelS, Resource rootResource, Resource childResource, JsonArray ontologyLD) {
		String rootGOLabel = root.getID();
		String nodeGOLabel = nodeLabelS;
		if(root.getID().startsWith("GO")) {
			//GO term 			
			String [] parts = root.getID().split("GO");
			String rootGOURI = "http://purl.obolibrary.org/obo/GO_"+parts[1];
			Resource rootGOResource;
			if(model.getResource(rootGOURI)!=null) {
				//already exists
				rootGOResource = model.getResource(rootGOURI);
			}
			else {
				//create the resource 
				rootGOResource = model.createResource(rootGOURI);
			}
			rootResource.addProperty(is_about, rootGOResource);
			rootGOLabel = findLabel(ontologyLD, rootGOURI);
		}
		
		if(nodeLabelS.startsWith("GO")) {
			//GO term 
			String [] parts = nodeLabelS.split("GO");
			String nodeGOURI = "http://purl.obolibrary.org/obo/GO_"+parts[1];
			Resource nodeGOResource;
			if(model.getResource(nodeGOURI)!=null) {
				//already exists
				nodeGOResource = model.getResource(nodeGOURI);
			}
			else {
				//create the resource 
				nodeGOResource = model.createResource(nodeGOURI);
			}
			childResource.addProperty(is_about, nodeGOResource);	
			nodeGOLabel = findLabel(ontologyLD, nodeGOURI);
		}
		return rootGOLabel+"/"+nodeGOLabel;
	}
	public static void annotateTree(ClassTerm root, Resource rootResource, String extentionLabel, JsonArray ontologyLD) {
		ArrayList<ClassTerm> children = root.getChildren();
		for (ClassTerm child : children) {
			String[] nameParts = child.getID().split("/");
			String nodeLabelS = nameParts[nameParts.length - 1];
			String childLabel = nodeLabelS + "-" + extentionLabel;
			
			Resource childResource = createResource(namedTreeNodeComponent, childLabel).addLiteral(nodeLabel,
					nodeLabelS);
			rootResource.addProperty(hasNodeComponent, childResource);	
			if(!hierarchy.equals("")) {
				hierarchy +=",";
			}
			String str = annotateGOTerms(root, nodeLabelS, rootResource, childResource, ontologyLD);
//			System.out.println("root: "+root.getID()+" node: "+nodeLabelS);
			System.out.println(str);
			hierarchy +=str;
//			System.out.println(hierarchy);
			annotateTree(child, childResource, extentionLabel, ontologyLD);
		}

	}

	public static Resource annotateAlternativeComponent(JSONObject alternativeComponent, String extentionLabel,
			Resource targetAttributeDtypeResource, ClusAttrType[] targets, String[] targetNames, String task) {
		String componentLabel = "targetDtypeAC:" + (String) alternativeComponent.get("label") + " | " + extentionLabel;
		Resource ontoACResource = model.createResource((String) alternativeComponent.get("URI"));
		Resource componentResource = createResource(ontoACResource, componentLabel);
		targetAttributeDtypeResource.addProperty(hasAlternativeComponent, componentResource);

		JSONObject datatypeObject = (JSONObject) alternativeComponent.get("is_datatype_role_of");
		String datatypeLabel = "Alternative Component Datatype: " + datatypeObject.get("label") + " | "
				+ extentionLabel;
		Resource ontoDTResource = model.createResource((String) datatypeObject.get("URI"));
		Resource datatypeResource = createResource(ontoDTResource, datatypeLabel);
		componentResource.addProperty(datatypeRoleOf, datatypeResource);

		// continue with datatypeResource

		// the following is executed when the task is TS
		if (task == "TS" && datatypeObject.get("has_base_datatype") != null) {
			datatypeObject = (JSONObject) datatypeObject.get("has_base_datatype");
			String baseLabel1 = "base_datatype" + extentionLabel + "|" + (String) datatypeObject.get("label");
			String baseURI1 = URIprefix + stringToHash(baseLabel1);
			Resource ontoBaseResource1 = model.createResource((String) datatypeObject.get("URI"))
					.addProperty(RDFS.label, (String) datatypeObject.get("label"));
			Resource baseResource1 = model.createResource(baseURI1).addProperty(RDFS.label, baseLabel1)
					.addProperty(RDF.type, ontoBaseResource1);
			datatypeResource.addProperty(hasBaseDatatype, baseResource1);

		}
		if (datatypeObject.get("has_field_component") != null) {
			JSONObject FCObject = (JSONObject) datatypeObject.get("has_field_component");
			JSONObject FCDataType = (JSONObject) FCObject.get("is_datatype_role_of");
			for (int i = 0; i < targets.length; i++) {
				String targetName = targetNames[i];
				String targetAttributeFCLabel = "targetAttribute-" + targetName + "FC-" + (String) FCObject.get("label")
						+ " | " + extentionLabel;
				Resource ontoFCResource = model.createResource((String) FCObject.get("URI"));
				Resource targetAttributeFCResource = createResource(ontoFCResource, targetAttributeFCLabel);
				datatypeResource.addProperty(hasFieldComponent, targetAttributeFCResource);

				String targetAttributeIDLabel = "targetAttribute-" + targetName + "ID-" + (String) FCObject.get("label")
						+ " | " + extentionLabel;
				Resource targetAttributeIDResource = createResource(fieldIdentifier, targetAttributeIDLabel);
				targetAttributeFCResource.addProperty(hasIdentifier, targetAttributeIDResource);

				String targetAttributeDtypeLabel = "targetAttribute-" + targetName + "Dtype-"
						+ (String) FCDataType.get("label") + " | " + extentionLabel;
				Resource ontoFCDTResource = model.createResource((String) FCDataType.get("URI"));
				Resource targetAttributeDtypeResourceSecond = createResource(ontoFCDTResource,
						targetAttributeDtypeLabel);
				targetAttributeFCResource.addProperty(datatypeRoleOf, targetAttributeDtypeResourceSecond);
				if (task == "MTMCC") {
					ClusAttrType target = targets[i];
					String[] discreteComponents = getDiscreteComponentsForAttribute(target);
					discreteDatatype(targetAttributeDtypeResourceSecond, extentionLabel, target.getName(),
							discreteComponents);
				}

			}

		}

		return datatypeResource;
	}

	public static String[] getComponents(String value) {
		value = value.replace("{", "");
		value = value.replace("}", "");
		value = value.trim();
		String[] components = value.split(",");
		return components;
	}

	// public static void printAllTarget(ClusAttrType[] targetAttributes) {
	// System.out.println("number of target attr is " + targetAttributes.length);
	// for (ClusAttrType clusAttrType : targetAttributes) {
	// System.out.println(clusAttrType.getName() + " " +
	// clusAttrType.getTypeName());
	// System.out.println(clusAttrType.getName());
	// }
	// System.out.println();
	// }

	public static String typeOfTask(ClusAttrType[] targetAttributes) {
		boolean allReals = true;
		if (targetAttributes.length == 1 && targetAttributes[0].getTypeName().equals("TimeSeries"))
			return "TS";
		if (targetAttributes.length == 1 && targetAttributes[0] instanceof clus.ext.hierarchical.ClassesAttrType) {
			ClassesAttrType target = (clus.ext.hierarchical.ClassesAttrType) targetAttributes[0];
			if (target.getHier().isTree()) {
				return "HMLC-tree";
			} else if (target.getHier().isDAG()) {
				return "HMLC-DAG";
			}
		}
		;

		for (ClusAttrType clusAttrType : targetAttributes) {
			if (!clusAttrType.getTypeName().equals("Numeric")) {
				allReals = false;
				break;
			}
		}
		if (allReals) {
			return targetAttributes.length > 1 ? "MTR" : "R";
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
		if (allbinary) {
			return targetAttributes.length > 1 ? "MLC" : "BC";
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
		if (mtc) {
			return targetAttributes.length > 1 ? "MTMCC" : "MCC";
		}
		if (!mtc && !allbinary && targetAttributes.length > 1) {
			return "MTC";
		}
		return "other";
	}

	public static void createRDFAll(JSONObject jsonObject) throws IOException, ClusException, java.text.ParseException {
		// String loc = "C:\\Users\\ana\\Google Drive\\bookChapter\\Clus3\\datasets";
//		String loc = "C:\\Users\\ana\\Desktop\\bookChapter\\Clus3\\HMC-test\\settings";
		String loc = "C:\\Users\\ana\\Desktop\\RepoSemanticDatasets\\e8datasets-master\\MLC\\newDatasets\\settings";
		File folder = new File(loc);
		File[] listOfFiles = folder.listFiles();
		for (File file : listOfFiles) {
			if (file.isFile() && file.getName().endsWith(".s")) {
				String[] settingsP = new String[1];
				settingsP[0] = file.getName();
				System.out.println("Settings file: " + settingsP[0]);
				String[] parts = file.getName().split("\\.s");
				createDatasetAnnotations(settingsP, "C:\\Users\\ana\\Desktop\\RepoSemanticDatasets\\TripleStore\\annotationsNewMLC",
						parts[0] + ".rdf", jsonObject);
				PrintStream bw = new PrintStream("C:\\Users\\ana\\Desktop\\RepoSemanticDatasets\\TripleStore\\annotationsNewMLC\\"+parts[0] + ".rdf");
				RDFDataMgr.write(bw, model, RDFFormat.RDFXML);
				model = ModelFactory.createDefaultModel();
			}
		}
	}
	public static void main(String[] args) throws IOException, ClusException, ParseException, java.text.ParseException {
		String jsonFilePath = "C:\\Users\\ana\\Desktop\\RepoSemanticDatasets\\Clus3\\DataJsonChanged.json";
		FileReader reader = new FileReader(jsonFilePath);
		JSONParser jsonParser = new JSONParser();
		JSONObject jsonObject = (JSONObject) jsonParser.parse(reader);
		createRDFAll(jsonObject);
		
		System.out.println("done");

	}
}