package clus;

import java.io.FileNotFoundException;
import java.io.FileReader;
import java.io.PrintStream;
import java.text.ParseException;
import java.text.SimpleDateFormat;
import java.util.ArrayList;
import java.util.Date;

import org.apache.jena.ontology.OntModel;
import org.apache.jena.ontology.OntModelSpec;
import org.apache.jena.ontology.OntProperty;
import org.apache.jena.rdf.model.Model;
import org.apache.jena.rdf.model.ModelFactory;
import org.apache.jena.rdf.model.Resource;
import org.apache.jena.riot.RDFDataMgr;
import org.apache.jena.riot.RDFFormat;

import com.google.gson.JsonArray;
import com.google.gson.JsonIOException;
import com.google.gson.JsonParser;
import com.google.gson.JsonSyntaxException;

import clus.data.type.ClusAttrType;
import clus.data.type.ClusSchema;

public class ForestryAnnotations {
	ClusSchema schema;
	Annotator annotator;
	public String URIprefix = "http://ontodm.com/SemanticAnnotation#";
	public Model forestryModel;
	public Model mainModel;
	String datasetName;
	public JsonArray ontologyJson;
	ArrayList<ClusAttrType> attributes;
	OntProperty segmentSize;
	OntProperty observedOnTimePoint;
	OntProperty hosts;
	OntProperty isObservedBy;
	OntProperty hasSpecifiedInput;
	OntProperty hasSpecifiedOutput;
	OntProperty fromDomain;
	OntProperty ofSegmentation;
	OntProperty isAbout;
	SimpleDateFormat format = new SimpleDateFormat("yyyy-MM-dd");
	Resource domainResource = annotator.createResourceString(
			annotator.findURI(ontologyJson, "Earth observations from space/remote sensing"),
			"Earth observations from space/remote sensing");

	public void addProperties() {
		OntModel ontModel = ModelFactory.createOntologyModel(OntModelSpec.OWL_DL_MEM);
		segmentSize = ontModel.createDatatypeProperty(annotator.findURI(ontologyJson, "segmentSize"));
		observedOnTimePoint = ontModel.createDatatypeProperty(annotator.findURI(ontologyJson, "observedOnTimePoint"));
		hosts = ontModel.createObjectProperty(annotator.findURI(ontologyJson, "hosts"));
		isObservedBy = ontModel.createObjectProperty(annotator.findURI(ontologyJson, "is_observed_by"));
		hasSpecifiedInput = ontModel.createObjectProperty(annotator.findURI(ontologyJson, "has_specified_input"));
		hasSpecifiedOutput = ontModel.createObjectProperty(annotator.findURI(ontologyJson, "has_specified_output"));
		fromDomain = ontModel.createObjectProperty(annotator.findURI(ontologyJson, "from_domain"));
		ofSegmentation = ontModel.createObjectProperty(annotator.findURI(ontologyJson, "of_segmentation"));
		isAbout = ontModel.createObjectProperty(annotator.findURI(ontologyJson, "is_about"));
		forestryModel.add(ontModel);
	}

	public ForestryAnnotations(Model mainModel, ClusSchema schema, String datasetName)
			throws JsonIOException, JsonSyntaxException, FileNotFoundException {
		Object obj = new JsonParser().parse(new FileReader("C:\\Users\\ana\\Google Drive\\Forestry\\Forest-LD.owl"));
		this.ontologyJson = (JsonArray) obj;
		this.forestryModel = ModelFactory.createDefaultModel();
		this.annotator = new Annotator(this.forestryModel, URIprefix);
		this.schema = schema;
		this.datasetName = datasetName;
		this.mainModel = mainModel;
		this.addProperties();

		attributes = new ArrayList<>();
		ClusAttrType[] descrAttributes = schema.getDescriptiveAttributes();
		for (ClusAttrType descAttrType : descrAttributes) {
			attributes.add(descAttrType);
		}
		ClusAttrType[] targAttributes = schema.getTargetAttributes();
		for (ClusAttrType targAttrType : targAttributes) {
			attributes.add(targAttrType);
		}
	}

	public void annotateDataset() throws ParseException, FileNotFoundException {
		switch (this.datasetName) {
		case "Forestry_Kras":
			this.annotateKras();
			break;
		case "SlivnicaLiDAR_Spot":
			this.annotateSlivnicaLiDAR_Spot();
			break;
		case "SlivnicaLiDAR_IRS":
			this.annotateSlivnicaLiDAR_IRS();
			break;
		case "SlivnicaLiDAR_Landsat":
			this.annotateSlivnicaLiDAR_Landsat();
			break;
		default:
			break;
		}
	}

	public void writeModel() throws FileNotFoundException {
		PrintStream bw = new PrintStream(
				"C:\\Users\\ana\\Desktop\\bookChapter\\TripleStore\\" + this.datasetName + ".rdf");
		RDFDataMgr.write(bw, this.forestryModel, RDFFormat.RDFXML);
	}

	public void annotateKras() throws ParseException, FileNotFoundException {
		Resource s1Resource = annotator
				.createResourceString(annotator.findURI(ontologyJson, "image segmentation specification"),
						datasetName + ":s1")
				.addLiteral(segmentSize, 4);
//		4ha and 20ha
		Resource s2Resource = annotator
				.createResourceString(annotator.findURI(ontologyJson, "image segmentation specification"),
						datasetName + ":s2")
				.addLiteral(segmentSize, 20);
		Resource platformResource = annotator.createResourceString(annotator.findURI(ontologyJson, "SOSA: platform"),
				datasetName + ":Landsat 7 ETM");
		Resource channel2Resource = annotator.createResourceString(annotator.findURI(ontologyJson, "SOSA: Sensor"),
				datasetName + ":Landsat 7 ETM" + ":channel2");
		Resource channel3Resource = annotator.createResourceString(annotator.findURI(ontologyJson, "SOSA: Sensor"),
				datasetName + ":Landsat 7 ETM" + ":channel3");
		Resource channel4Resource = annotator.createResourceString(annotator.findURI(ontologyJson, "SOSA: Sensor"),
				datasetName + ":Landsat 7 ETM" + ":channel4");
		Resource channel5Resource = annotator.createResourceString(annotator.findURI(ontologyJson, "SOSA: Sensor"),
				datasetName + ":Landsat 7 ETM" + ":channel5");
		Resource channel7Resource = annotator.createResourceString(annotator.findURI(ontologyJson, "SOSA: Sensor"),
				datasetName + ":Landsat 7 ETM" + ":channel7");
		platformResource.addProperty(hosts, channel2Resource);
		platformResource.addProperty(hosts, channel3Resource);
		platformResource.addProperty(hosts, channel4Resource);
		platformResource.addProperty(hosts, channel5Resource);
		platformResource.addProperty(hosts, channel7Resource);

		for (ClusAttrType attribute : attributes) {
			String attributeName = attribute.getName();
			Resource featureSpecificationResource = annotator.getResourceFromModel(mainModel,
					datasetName + ":" + attributeName + ":featureSpecification");
			switch (attributeName) {
			case "sklep":
				break;
			case "ndsm":
				break;
			case "delveg":
				break;
			case "vpv1_hmx":
				break;
			case "vpv1_h99":
				break;
			case "vpv1_h95":
				break;
			case "vpv1_h75":
				break;
			case "vpv1_h50":
				break;
			case "vpv1_h25":
				break;
			case "vpv1_h10":
				break;
			case "vpv1_h05":
				break;

			default: {
				// descriptive features
				String[] parts = attributeName.split("_");

				String segmentation = Character.toString(parts[0].charAt(2)) + Character.toString(parts[0].charAt(3));
				Resource currentSegmentationResource = null;
				if (segmentation.equals("s1"))
					currentSegmentationResource = s1Resource;
				else if (segmentation.equals("s2"))
					currentSegmentationResource = s2Resource;

				String dateString = Character.toString(parts[0].charAt(0));
				Date date = new Date();
				switch (dateString) {
					case "a": date = format.parse("2001-08-03"); break;
					case "b": date = format.parse("2002-05-18"); break;
					case "c": date = format.parse("2002-11-10"); break;
					case "d": date = format.parse("2003-03-18"); break;
					default: break;
				}

				String statisticAggregation = parts[1];
				String statisticAggregationOntologyLabel = getStatisticalAggregationFullLabel(statisticAggregation);

				String channel = Character.toString(parts[0].charAt(1));
				Resource currentChannelResource = null;
				switch (channel) {
					case "2": currentChannelResource = channel2Resource; break;
					case "3": currentChannelResource = channel3Resource; break;
					case "4": currentChannelResource = channel4Resource; break;
					case "5": currentChannelResource = channel5Resource; break;
					case "7": currentChannelResource = channel7Resource; break;
					default: break;
				}

				annotateAggregatedProperties(attributeName, date, currentChannelResource, currentSegmentationResource,
						statisticAggregationOntologyLabel, featureSpecificationResource, "reflectance");
				break;
			}
			}

		}
	}

	public void annotateSlivnicaLiDAR_Spot() throws ParseException {
		Resource platformResource = annotator.createResourceString(annotator.findURI(ontologyJson, "SOSA: platform"),
				datasetName + ":SPOT");
		Resource channel1Resource = annotator.createResourceString(annotator.findURI(ontologyJson, "SOSA: Sensor"),
				datasetName + ":SPOT" + ":channel3");
		Resource channel2Resource = annotator.createResourceString(annotator.findURI(ontologyJson, "SOSA: Sensor"),
				datasetName + ":SPOT" + ":channel4");
		Resource channel3Resource = annotator.createResourceString(annotator.findURI(ontologyJson, "SOSA: Sensor"),
				datasetName + ":SPOT" + ":channel5");
		Resource channel4Resource = annotator.createResourceString(annotator.findURI(ontologyJson, "SOSA: Sensor"),
				datasetName +":SPOT" + ":channel7");
		platformResource.addProperty(hosts, channel1Resource);
		platformResource.addProperty(hosts, channel2Resource);
		platformResource.addProperty(hosts, channel3Resource);
		platformResource.addProperty(hosts, channel4Resource);

		for (ClusAttrType attribute : attributes) {
			String attributeName = attribute.getName();
			Resource featureSpecificationResource = annotator.getResourceFromModel(mainModel,
					datasetName + ":" + attributeName + ":featureSpecification");
			switch (attributeName) {
				case "h":
					break;
				case "p":
					break;
				case "aspect":
					break;
	
				default: {
					// descriptive features
					String[] parts = attributeName.split("_");
					String statisticAggregation;
					statisticAggregation = parts[0];
					String statisticAggregationOntologyLabel = getStatisticalAggregationFullLabel(statisticAggregation);
					
					String quality = null;
					Date date = null;
					Resource currentSegmentationResource = null;
					Resource currentChannelResource = null;
					
					Character dateType = null;
					String channel = null;
					
					String variable = parts[1];
					if (variable.equals("dmr")) quality = "dmr";
					else if(variable.equals("slope")) quality = "NCIT: slope";
					else if(parts[0].equals("ndvi")) {
						quality = "Normalized Difference Vegetation Index (NDVI)";
						dateType = parts[2].charAt(parts[2].length()-1);
					}
				    else {
				    	quality = "reflectance";
				    	
				    	if(variable.equals("spot")) {
				    		dateType = '2';
				    		channel =parts[3];
				    	}
				    	else {
//				    		ex min_spot4
				    		dateType = '1';
				    		channel = Character.toString(parts[1].charAt(parts.length - 1));
				    	}					
					}
					
					switch (channel) {
						case "1": currentChannelResource = channel1Resource; break;
						case "2": currentChannelResource = channel2Resource; break;
						case "3": currentChannelResource = channel3Resource; break;
						case "4": currentChannelResource = channel4Resource; break;
						default: break;
					}
					
					if(dateType == '1') date = format.parse("2006-09-03");
					if(dateType == '2') date = format.parse("2006-09-23");
					
					annotateAggregatedProperties(attributeName, date, currentChannelResource, currentSegmentationResource,
							statisticAggregationOntologyLabel, featureSpecificationResource, quality);
					
					break;
				}
			}

		}

	}

	public void annotateSlivnicaLiDAR_IRS() throws ParseException {
		Resource platformResource = annotator.createResourceString(annotator.findURI(ontologyJson, "SOSA: platform"),
				datasetName + ":IRS P6 LISS III");
		Resource channel1Resource = annotator.createResourceString(annotator.findURI(ontologyJson, "SOSA: Sensor"),
				datasetName + ":IRS P6 LISS III" + ":channel1");
		Resource channel2Resource = annotator.createResourceString(annotator.findURI(ontologyJson, "SOSA: Sensor"),
				datasetName + ":IRS P6 LISS III" + ":channel2");
		Resource channel3Resource = annotator.createResourceString(annotator.findURI(ontologyJson, "SOSA: Sensor"),
				datasetName + ":IRS P6 LISS III" + ":channel3");
		Resource channel4Resource = annotator.createResourceString(annotator.findURI(ontologyJson, "SOSA: Sensor"),
				datasetName + ":IRS P6 LISS III" + ":channel4");
		platformResource.addProperty(hosts, channel1Resource);
		platformResource.addProperty(hosts, channel2Resource);
		platformResource.addProperty(hosts, channel3Resource);
		platformResource.addProperty(hosts, channel4Resource);

		for (ClusAttrType attribute : attributes) {
			String attributeName = attribute.getName();
			Resource featureSpecificationResource = annotator.getResourceFromModel(mainModel,
					datasetName + ":" + attributeName + ":featureSpecification");
			switch (attributeName) {
				case "h":
					break;
				case "p":
					break;
				case "aspect":
					break;
	
				default: {
					// descriptive features
					String[] parts = attributeName.split("_");
					
					String statisticAggregation;
					statisticAggregation = parts[0];
					String statisticAggregationOntologyLabel = getStatisticalAggregationFullLabel(statisticAggregation);
					
					Date date = null;
					date = format.parse("2006-07-17");
					
					
					Resource currentChannelResource = null;
					String quality = null;
					Resource currentSegmentationResource = null;
					
					String variable = parts[1];
					if (variable.equals("dmr")) quality = "dmr";
					else if (variable.equals("slope")) quality = "NCIT: slope";
					else if (variable.equals("ndvi")) quality = "Normalized Difference Vegetation Index (NDVI)";
					else {
						quality = "reflectance";
						String channel = Character.toString(parts[1].charAt(parts.length - 1));
						switch (channel) {
						case "1": currentChannelResource = channel1Resource; break;
						case "2": currentChannelResource = channel2Resource; break;
						case "3": currentChannelResource = channel3Resource; break;
						case "4": currentChannelResource = channel4Resource; break;
						default: break;
						}
					}
						
					annotateAggregatedProperties(attributeName, date, currentChannelResource, currentSegmentationResource,
							statisticAggregationOntologyLabel, featureSpecificationResource, quality);
					
					break;
				}
			}
		}

	}

	public String getStatisticalAggregationFullLabel(String statisticAggregation) {
		String statisticAggregationOntologyLabel = null;
		switch (statisticAggregation) {
		case "min":
			statisticAggregationOntologyLabel = "STATO: minimum value";
			break;
		case "max":
			statisticAggregationOntologyLabel = "STATO: maximum value";
			break;
		case "avg":
			statisticAggregationOntologyLabel = "STATO: average value";
			break;
		case "std":
		case "stddev":
			statisticAggregationOntologyLabel = "STATO: standard deviation";
			break;
		default:
			break;
		}
		return statisticAggregationOntologyLabel;
	}

	public void annotateAggregatedProperties(String attributeName, Date date, Resource currentChannelResource,
			Resource currentSegmentationResource, String statisticAggregationOntologyLabel,
			Resource featureSpecificationResource, String quality) {

		Resource propertyResource = annotator.createResourceString(annotator.findURI(ontologyJson, quality),
				datasetName + ":" + attributeName + ":" + quality).addProperty(fromDomain, domainResource);
		if (date != null)
			propertyResource.addLiteral(observedOnTimePoint, date);
		if (currentChannelResource != null)
			propertyResource.addProperty(isObservedBy, currentChannelResource);
		if (currentSegmentationResource != null)
			propertyResource.addProperty(ofSegmentation, currentSegmentationResource);
		Resource aggregatedProperty = annotator.createResourceString(
				annotator.findURI(ontologyJson, statisticAggregationOntologyLabel),
				datasetName + ":" + attributeName + ":" + statisticAggregationOntologyLabel);
		@SuppressWarnings("unused")
		Resource propertyAggregation = annotator
				.createResourceString(annotator.findURI(ontologyJson, "EO property aggregation"),
						datasetName + ":" + attributeName + ":EOpropertyAggregation")
				.addProperty(hasSpecifiedInput, propertyResource).addProperty(hasSpecifiedOutput, aggregatedProperty);
		featureSpecificationResource.addProperty(isAbout, propertyResource);

	}

	public void annotateSlivnicaLiDAR_Landsat() throws ParseException {
		Resource s3Resource = annotator
				.createResourceString(annotator.findURI(ontologyJson, "image segmentation specification"),
						datasetName + ":s3")
				.addLiteral(segmentSize, 17577);
		Resource platformResource = annotator.createResourceString(annotator.findURI(ontologyJson, "SOSA: platform"),
				datasetName + ":Landsat 7 ETM");
		Resource channel3Resource = annotator.createResourceString(annotator.findURI(ontologyJson, "SOSA: Sensor"),
				datasetName + ":Landsat 7 ETM" + ":channel3");
		Resource channel4Resource = annotator.createResourceString(annotator.findURI(ontologyJson, "SOSA: Sensor"),
				datasetName + ":Landsat 7 ETM" + ":channel4");
		Resource channel5Resource = annotator.createResourceString(annotator.findURI(ontologyJson, "SOSA: Sensor"),
				datasetName + ":Landsat 7 ETM" + ":channel5");
		Resource channel7Resource = annotator.createResourceString(annotator.findURI(ontologyJson, "SOSA: Sensor"),
				datasetName + ":Landsat 7 ETM" + ":channel7");
		platformResource.addProperty(hosts, channel3Resource);
		platformResource.addProperty(hosts, channel4Resource);
		platformResource.addProperty(hosts, channel5Resource);
		platformResource.addProperty(hosts, channel7Resource);

		for (ClusAttrType attribute : attributes) {
			String attributeName = attribute.getName();
			Resource featureSpecificationResource = annotator.getResourceFromModel(mainModel,
					datasetName + ":" + attributeName + ":featureSpecification");
			switch (attributeName) {
			case "h":
				break;
			case "p":
				break;
			case "aspect":
				break;

			default: {
				// descriptive features
				String quality = null;
				Date date = null;
				String statisticAggregationOntologyLabel = null;				
				Resource currentChannelResource = null;
				
				String[] parts = attributeName.split("_");
				if (parts.length == 2) {
					String statisticAggregation;
					statisticAggregation = parts[0];
					statisticAggregationOntologyLabel = getStatisticalAggregationFullLabel(statisticAggregation);
					String variable = parts[1];
					if (variable.equals("dmr")) quality = "dmr";
					else if (variable.equals("slope")) quality = "NCIT: slope";
				} else {
					String statisticAggregation = parts[2];
					statisticAggregationOntologyLabel = getStatisticalAggregationFullLabel(statisticAggregation);
					String dateString = parts[1];
					switch (dateString) {
						case "1995": date = format.parse("1995-07-26"); break;
						case "1996": date = format.parse("1996-06-03"); break;
						case "2000": date = format.parse("2000-09-10"); break;
						case "2001": date = format.parse("2001-08-03"); break;
						case "2002": date = format.parse("2002-05-18"); break;
//						 what do we do with the second date in 2002?
//						 case "2001": date = format.parse("2002-11-10"); break;
						case "2003": date = format.parse("2003-03-18"); break;
						default: break;
					}

					if (parts[0].equals("ndvi")) {
						quality = "Normalized Difference Vegetation Index (NDVI)";
					} else {
						// its band regular feature
						quality = "reflectance";
						String channel = Character.toString(parts[0].charAt(parts.length - 1));
						switch (channel) {
							case "3": currentChannelResource = channel3Resource; break;
							case "4": currentChannelResource = channel4Resource; break;
							case "5": currentChannelResource = channel5Resource; break;
							case "7": currentChannelResource = channel7Resource; break;
							default: break;
						}

					}
					
				}
				annotateAggregatedProperties(attributeName, date, currentChannelResource, s3Resource,
						statisticAggregationOntologyLabel, featureSpecificationResource, quality);
				break;
			}
			}

		}

	}

}
