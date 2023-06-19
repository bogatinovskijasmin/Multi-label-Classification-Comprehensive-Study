import { Renderer2, Component, Input, ViewChild, OnInit, Inject } from '@angular/core';
import { ActivatedRoute } from '@angular/router';
import { MatPaginator, MatTableDataSource, MatSort } from '@angular/material';
import { Ng4LoadingSpinnerService } from 'ng4-loading-spinner';
import {DataService} from '..//data.service';
import {Creator} from '../utlis/Creator';
import { DOCUMENT } from '@angular/common';
import { element } from '@angular/core/src/render3';

@Component({
  selector: 'app-dataset',
  templateUrl: './dataset.component.html',
  styleUrls: ['./dataset.component.css']
})

export class DatasetComponent implements OnInit{
  name: any;
  public label: string;
  description: string = "";
  license: string = "";
  keywords: string = "";
  title: string = "";
  sameAsArray: [] = [];
  identifierArray: [] = [];
  creatorArray: Creator [] = [];
  mlcLabelsArray: String [] = [];

  schema = {
    '@context': 'http://schema.org',
    '@type': 'WebSite',
    'name': 'angular.io',
    'url': 'https://angular.io'
  };

  constructor(private _renderer2: Renderer2 ,  @Inject(DOCUMENT) private _document: Document, private route: ActivatedRoute, private spinnerService: Ng4LoadingSpinnerService, private dataService: DataService) { }

  @ViewChild('paginatorMeta') paginatorMeta: MatPaginator;
  @ViewChild('sorterMeta') sorterMeta: MatSort;
  @ViewChild('paginatorFeatures') paginatorFeatures: MatPaginator;
  @ViewChild('sorterFeatures') sorterFeatures: MatSort;
  displayedColumnsMeta: string[] = ['mfLabel', 'mfValue'];
  displayedColumnsFeatures: string[] = ['featureName', 'featureType', 'boxplot'];
  dataSourceFeatures:any;
  barData:any[]=[];
  dataSourceMeta:any;
  query: string;
  
  metaFeaturesTrainPath = "";
  metaFeaturesTestPath = ""

  trainDatasetPath ="";
  testDatasetPath ="";
  annotationsPath = "";


  ngOnInit() {
    //set table 
    this.dataSourceFeatures = new MatTableDataSource(this.dataSourceFeatures);
    this.dataSourceMeta = new MatTableDataSource(this.dataSourceMeta);
    this.dataSourceFeatures.sort = this.sorterFeatures;
    this.dataSourceFeatures.paginator = this.paginatorFeatures;
    this.dataSourceMeta.sort = this.sorterMeta;
    this.dataSourceMeta.paginator = this.paginatorMeta;

    //set parameters 
    this.route.paramMap.subscribe(params => {
    console.log(params.get('name'))
    this.name = params.get('name');
    });

    //set dataset label 
    this.setDatasetLabel();

    

    //load meta features
    this.loadMetaFeatures();

    
    

    this.mlcLabels();

  }


  mlcLabels(){
    var queryTarget = "";
    queryTarget = queryTarget.concat(
      `PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
      PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
      PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>
      SELECT distinct ?cha
      WHERE {
      # dset <-is-about ds
        ?dsInstance <http://purl.obolibrary.org/obo/IAO_0000136>  <`+this.name+`> .
        ?dsInstance <http://www.obofoundry.org/ro/ro.owl#has_part> ?dTypeInstance. 
        ?dTypeInstance <http://www.ontodm.com/OntoDT/OntoDT_80000000> ?targFCInstance. 
        ?targFCInstance rdf:type ?targFCClass .
        ?targFCClass rdfs:subClassOf <http://www.ontodm.com/OntoDT#OntoDT_8c7ab50e_e725_47f8_be3e_b14b257f8bbe> .
        ?targFCInstance <http://ontodm.com/OntoDT#OntoDT_0000010> ?targDtypeInstance. 
        ?targDtypeInstance <http://www.ontodm.com/OntoDT/OntoDT_80000004> ?targetDiscreteDT.
        ?targDtypeInstance <http://ontodm.com/SemanticAnnotation#featureCharacteristics> ?cha.
      }`
    )
    this.executeTargetQuery(queryTarget);
  }

  setFeatures(){
    var queryFeatures = "";
    queryFeatures = queryFeatures.concat(
      "PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>\n"+
      "PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>\n"+
      "PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>\n"+
      "SELECT ?featureName ?featureType ?featureCharacteristic\n"+
      "WHERE {\n"+
      "# dset <-is-about ds\n"+
      "  ?dsInstance <http://purl.obolibrary.org/obo/IAO_0000136>  <"+this.name+"> .\n"+
      "  ?dsInstance <http://www.obofoundry.org/ro/ro.owl#has_part> ?dTypeInstance. \n"+
      "  ?dTypeInstance <http://www.ontodm.com/OntoDT/OntoDT_80000000> ?descFCInstance. \n"+
      "  ?descFCInstance rdf:type ?descFCClass .\n"+
      "  ?descFCClass rdfs:subClassOf <http://www.ontodm.com/OntoDT#OntoDT_47a7dfda_6531_4182_b5e7_c275c9861f34> .\n"+
      "  ?descFCInstance <http://ontodm.com/OntoDT#OntoDT_0000010> ?descDtypeInstance. \n"+
      "  ?descDtypeInstance <http://www.ontodm.com/OntoDT/OntoDT_80000000> ?featureFCInstance. \n"+
      "  ?featureFCInstance <http://ontodm.com/OntoDT#OntoDT_0000010> ?featureInstance.\n"+
      "  ?featureInstance <http://ontodm.com/SemanticAnnotation#featureName> ?featureName. \n"+
      "  ?featureInstance <http://ontodm.com/SemanticAnnotation#featureType> ?featureType.\n"+
      "  ?featureInstance <http://ontodm.com/SemanticAnnotation#featureCharacteristics> ?featureCharacteristic. \n"+
      "}\n"
    )

    console.log("Feature query:"+queryFeatures)

    this.executeFeatureQuery(queryFeatures);

  }

  getProvenace(){
    var queryProvenance = "";
    queryProvenance = queryProvenance.concat(
      "PREFIX schema: <https://schema.org/>\n"+
      "SELECT  ?name ?keywords ?description ?license (group_concat(DISTINCT ?sameAsInstance; separator =',') as ?sameAs) (group_concat(DISTINCT ?identifierInstance; separator =',') as ?identifier) \n"+
      "WHERE { \n"+
      "  <"+this.name+"> schema:name ?name .\n"+
      "  <"+this.name+"> schema:keywords ?keywords.\n"+
      "  <"+this.name+"> schema:description ?description.\n"+
      "  <"+this.name+"> schema:license ?license.\n"+
      "  <"+this.name+"> schema:sameAs ?sameAsInstance.\n"+
      "  <"+this.name+"> schema:identifier ?identifierInstance.\n"+
      "}	\n"+
      "group by ?name ?keywords ?description ?license\n"
    )
    console.log("provenance:");
    console.log(queryProvenance);
    this.executeProvenanceQuery(queryProvenance);
    this.getDatasetCreators();
  }

  executeProvenanceQuery = function(query){
    this.dataService.getResults(query).subscribe(res => {
      var elem = res.results.bindings[0];
      if(elem!=undefined){
        //there is some provenance information
        if(elem.description!=undefined)
        this.description = elem.description.value;
        if(elem.name!=undefined){
          this.title = elem.name.value;
        }
        if(elem.license!=undefined&&elem.license!="na"){
          this.license = elem.license.value;
        }
        if(elem.keywords!=undefined)
          this.keywords = elem.keywords.value;
          elem.sameAs.value.split(",").forEach(element => {
            this.sameAsArray.push(element);
          });
        if(elem.identifier!=undefined)
          elem.identifier.value.split(",").forEach(element => {
            this.identifierArray.push(element);
          });
          
      }
      else{
        this.title = this.label.split("-")[0]; 
      }

      //set meta feature path
      this.metaFeaturesTrainPath="ftp://semantichub.ijs.si/ftp/datasets/MLC/metaFeaturesJsonFiles/"+this.title+"_train.json";
      this.metaFeaturesTestPath="ftp://semantichub.ijs.si/ftp/datasets/MLC/metaFeaturesJsonFiles/"+this.title+"_test.json";
      this.trainDatasetPath = "ftp://semantichub.ijs.si/ftp/datasets/MLC/MLC-Datasets/"+this.title+"/"+this.title+"_train"+".arff";
      this.testDatasetPath = "ftp://semantichub.ijs.si/ftp/datasets/MLC/MLC-Datasets/"+this.title+"/"+this.title+"_test"+".arff";
      this.annotationsPath = "ftp://semantichub.ijs.si/ftp/datasets/MLC/annotations/"+this.title+".rdf";
    })
  }

  getDatasetCreators(){
    var queryCreator = "";
    queryCreator = queryCreator.concat(
      "PREFIX schema: <https://schema.org/>\n"+
      "SELECT ?creatorName ?creatorURL\n"+
      "WHERE { \n"+
      "  <"+this.name+"> schema:creator ?creator .\n"+
      "  ?creator schema:name ?creatorName.\n"+
      "  ?creator schema:url ?creatorURL.\n"+
      "}\n"	
    )
    this.executeCreatorQuery(queryCreator);
  }

  executeCreatorQuery = function(query){
    this.dataService.getResults(query).subscribe(res => {
      var elem = res.results.bindings[0];
      if(elem!=undefined){
        var creator = new Creator(elem.creatorName.value, elem.creatorURL.value);
        this.creatorArray.push(creator);
      }
      console.log("creator: "+this.creatorArray)

    })
  }
  

  executeFeatureQuery = function(query){
    console.log(query);
    this.spinnerService.show();
    this.dataService.getResults(query).subscribe(res => {  
      console.log("Features: ");
      console.log(res.results); 
      this.dataSourceFeatures = new MatTableDataSource(this.formatFeatureArray(res));
      this.dataSourceFeatures.paginator = this.paginatorFeatures;
      this.dataSourceFeatures.sort = this.sorterFeatures; 
      this.spinnerService.hide();
    });
  }

  executeTargetQuery = function(query){
    this.dataService.getResults(query).subscribe(res =>{
      this.barData = this.formatTargetArray(res)
    })
  }

  formatTargetArray = function(res){
    var xArray: String [] = [];
    var yArray: String [] = [];
    res.results.bindings.forEach(element=>{
      var temp = element.cha.value;
      var labels = temp.split(";");
      labels.forEach(label => {
        var parts1:String[] = label.split(":");
        xArray.push(parts1[0]);
        yArray.push(parts1[1].split(",")[0].split("=")[1]);
      });
    })
    var data = [{
      x: xArray,
      y: yArray,
      type: 'bar'
    }]
    return data;
  }
  // formatResult = function(num){
  //   if(isNaN(num)){
  //     return Number(0).toFixed(6);
  //   }
  //   else return Number(num).toFixed(6);
  // }
  formatFeatureArray = function (res, type) {
    var newArray = [];
    res.results.bindings.forEach(element => {
      var type = element.featureType.value;
      if(type == "numeric"){
        newArray.push({
          featureName: element.featureName.value,
          featureType: element.featureType.value, 
          featureCharacteristic: element.featureCharacteristic.value.split(","), 
        })
      }else
      if(type == "nominal"){
        var parts = element.featureCharacteristic.value.split(",")
        var labels:string[] = [];
        var values:string[] = [];
        parts.forEach(part=>{
          var temp = part.split("=");
          labels.push(temp[0].trim());
          values.push(temp[1]);
        });
        
        newArray.push({
          featureName: element.featureName.value,
          featureType: element.featureType.value, 
          featureLabeles: labels,
          featureValues: values 
        })
      }
      
      
    });
    return newArray;
  }

  setDatasetLabel(){
    var queryDSLabel = "";
    queryDSLabel = queryDSLabel.concat(
      "PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>\n"+
      "PREFIX OntoDM: <http://www.ontodm.com/OntoDM-core/>\n"+
      "SELECT DISTINCT ?datasetLabel\n"+
      "WHERE {\n"+
      "  <"+this.name+"> rdfs:label ?datasetLabel .  \n"+
      "}\n"
    );
    console.log("Query: "+queryDSLabel)
    this.dataService.getResults(queryDSLabel).subscribe(res => { 
      this.label = this.getLabel(res).split("dset:")[1];
      //load features
      this.setFeatures();
      //load provenance
      this.getProvenace();
      
    })
    
  }
  getLabel (res){
    return res.results.bindings[0].datasetLabel.value;
  }

  loadMetaFeatures(){
    this.query = "";
    this.query = this.query.concat(
      "SELECT ?mfLabel ?mfValue\n"+
      "WHERE {\n"+
      "  <"+this.name+"> <http://purl.obolibrary.org/obo/RO_0000086> ?mfInstance .\n"+
      "  ?mfInstance <http://www.ontodm.com/OntoDT#OntoDT_0000240> ?mfValue .\n"+
      "  ?mfInstance <http://ontodm.com/SemanticAnnotation#typeName> ?mfLabel .\n"+
      "}\n"
    );
    this.executeQuery(this.query);
  }

  executeQuery = function(query){
    console.log(query);
    this.spinnerService.show();
    this.dataService.getResults(query).subscribe(res => {  
      this.dataSourceMeta = new MatTableDataSource(this.formatResArray(res));
      // console.log(res.results);      
      this.dataSourceMeta.paginator = this.paginatorMeta;
      this.dataSourceMeta.sort = this.sortMeta; 
      this.spinnerService.hide();
    });
  }

  formatResult = function(num){
    if(isNaN(num)){
      return Number(0).toFixed(5);
    }
    else if(Number(num)%1!=0){
      //decimal
      return Number(num).toFixed(5);
    } 
    else {
      //whole number 
      return Number(num);
    }
  }

  formatResArray = function (res) {
    var newArray = [];
    res.results.bindings.forEach(element => {
      newArray.push({
        mfLabel: element.mfLabel.value,
        mfValue: this.formatResult(element.mfValue.value)
      })
      
    });
    return newArray;
  }

}