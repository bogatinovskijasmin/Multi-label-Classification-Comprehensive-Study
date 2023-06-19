import { Component, OnInit, ViewChild } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { FormBuilder, Validators, FormGroup } from '@angular/forms';
import { Ng4LoadingSpinnerService } from 'ng4-loading-spinner';
import {DataService} from '..//data.service';
import {BrowserAnimationsModule} from '@angular/platform-browser/animations';
import {MatCheckboxModule} from '@angular/material/checkbox';
import 'hammerjs';
import { Router } from '@angular/router';


@Component({
  selector: 'app-filter',
  templateUrl: './filter.component.html',
  styleUrls: ['./filter.component.css']
})
export class FilterComponent implements OnInit {

  constructor(private dataService: DataService, private router:Router, private http: HttpClient, private spinnerService: Ng4LoadingSpinnerService){
  }

  dropdownSettingsSingle = {
    singleSelection: true,
    idField: 'item_id',
    textField: 'item_text',
    selectAllText: 'Select All',
    unSelectAllText: 'UnSelect All',
    itemsShowLimit: 3,
    allowSearchFilter: true
  };

  
  onItemSelect(item: any) {
  }
  onSelectAll(items: any) {
  }
  
  values: number[];
  onFilterChange(value: string) {
    console.log('filter:', value);
  }
  filterEnabled: Boolean;
  query: string;
  metaQuery: string;
  selected1: string;
  selected2: string;
  selected4: string;
  ST: string;
  numberOfDescriptiveFeatures: string;
  numberOfTargetFeatures: string;
  isCollapsed: boolean;
  choices: any[]=[];
  mappings: any[]=[];
  targ: any;
  metaFeaturesMLC: string []=["DefaultAccuracy", "TotalDistinctClasses", "UnseenInTrain", "RatioTrainToPower", "RatioTestToPower", "RatioTotalToPower", "RatioUnseenToTest", "Attributes", "Distinct labelsets", "Instances", "Labels", "LxIxF", "Ratio of number of instances to the number of attributes", "Cardinality", "Density", "Maximal entropy of labels", "Mean of entropies of labels", "Minimal entropy of labels", "Standard deviation of label cardinality", "CVIR inter class", "Kurtosis cardinality", "Max IR inter class", "Max IR intra class", "Max IR per labelset", "Mean of IR inter class", "Mean of IR intra class", "Mean of IR per labelset", "Mean of standard deviation of IR intra class", "Proportion of maxim label combination (PMax)", "Proportion of unique label combination (PUniq)", "Skewness cardinality", "Average examples per labelset", "Bound", "Diversity", "Number of labelsets up to 10 examples", "Number of labelsets up to 2 examples", "Number of labelsets up to 50 examples", "Number of labelsets up to 5 examples", "Mean examples per labelset", "Number of unconditionally dependent label pairs by chi-square test", "Proportion of distinct labelsets", "Ratio of number of labelsets up to 10 examples", "Ratio of number of labelsets up to 2 examples", "Ratio of number of labelsets up to 50 examples", "Ratio of number of labelsets up to 5 examples", "Ratio of unconditionally dependent label pairs by chi-square test", "SCUMBLE", "Standard deviation of examples per labelset", "Number of unique labelsets", "Average gain ratio", "Number of binary attributes", "Mean of entropies of nominal attributes", "Mean of kurtosis", "Mean of mean of numeric attributes", "Mean of skewness of numeric attributes", "Mean of standard deviation of numeric attributes", "Number of nominal attributes", "Number of numeric attributes", "Proportion of binary attributes", "Proportion of nominal attributes", "Proportion of numeric attributes", "Proportion of numeric attributes with outliers"];

  dimension4: string[] = ['with missing', 'without missing'];  

  tasksFlat = [
    {text: 'multi-label classification', value: 'multi-label classification', checked: true, child:"one"}
  ];
    

  ngOnInit() {
    this.query = "";
    this.metaQuery = "";
    // this.numberOfDescriptiveFeatures = "";
    // this.addNewChoice();
  }
  addNewChoice = function(){
    var newItemNo = this.choices.length;
    this.choices.push({'id' :  newItemNo, 'name' : 'choice' + newItemNo});
    this.mappings.push( {'feature':undefined, 'range' : ""});
  }

  removeNewChoice = function(choice) {
    var id = choice.id;
    var index = -1;
    var i;
    for(i =0; i<this.choices.length; i++){
        if(this.choices[i].id==id){
            index = i;
            break;
        }
    }
    if(index!=-1){
      this.choices.splice(index, 1);
      this.mappings.splice(index, 1); 
    }
  };

  disableNewMapping = function(){
    var num = this.mappings.length;
    // /^(\d*(-\d+)?|[><]=?\d+)$/ old
    if(num>0 && (this.mappings[num-1].feature=="" || this.mappings[num-1].range=="" || /^(\d+(\.\d)?\d*(-\d+(\.\d)?\d*)?|[><]=?\d+(\.\d)?\d*)$/.test(this.mappings[num-1].range)==false)) return true;
    return false;
  }

  executeQuery = function(){
    this.router.navigateByUrl('/datasets-list', { state: {query: this.query, metaQuery: this.metaQuery, mappings: this.mappings } });
  }

  rangeFilter(item, feature){
      if(item.match(/\d+-\d+/)){
        //range
        var numbers = item.split("-");
        return feature+">="+numbers[0]+"&&"+feature+"<="+numbers[1];
      }
      else
      if(item.match(/^\d+/g)){
        //one number
       return  feature+"="+item;
      }
      else{
        //rest (<, >, >=, <=)
        return feature+item;
      }
  }

  createQuery(){
    this.query ="";
    var datasetSpecificationLabelString = "'multi-label classification dataset'@en" 
    var metaFeaturesStr: string = "";
    for (let i = 0; i<this.mappings.length; i++){
      var metaFeature = this.mappings[i];
      metaFeaturesStr = metaFeaturesStr.concat("(?mfLabel = '"+metaFeature.feature+"' && "+this.rangeFilter(metaFeature.range, "xsd:float(?mfValue)")+")");
      if(i<this.mappings.length-1){
        metaFeaturesStr = metaFeaturesStr.concat("||");
      }
    }
   
    this.query = this.buildQuery(metaFeaturesStr,datasetSpecificationLabelString, false);
    this.metaQuery = this.buildQuery(metaFeaturesStr,datasetSpecificationLabelString, true);
    this.executeQuery();
  }

  buildQuery(metaFeaturesStr, datasetSpecificationLabelString, isMeta){
    var queryL = "";
    queryL = queryL.concat(
      "PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>\n"+
      "PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>\n"+
      "PREFIX OntoDM: <http://www.ontodm.com/OntoDM-core/>\n"+
      "PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>\n");
    if(!isMeta){
      queryL = queryL.concat(
        "SELECT DISTINCT ?dsetInstance ?datasetLabel ?numTargets ?numDescriptive ?numInstances ?hasMissingValues\n"
      )
    }
    else{
      queryL = queryL.concat(
        "SELECT DISTINCT ?dsetInstance ?datasetLabel ?mfLabel ?mfValue\n"
      )
    }
    queryL = queryL.concat(
      "WHERE {\n"+
      "  ?dsetInstance rdf:type ?dsetClass .\n"+
      "  ?dsetClass rdfs:subClassOf <http://www.ontodm.com/OntoDM-core/OntoDM_000144> .\n"+
      "  ?dsetInstance rdfs:label ?datasetLabel .\n"+
      "  ?dsetInstance <http://ontodm.com/SemanticAnnotation#numOfTargets> ?numTargets .\n"+
      "  ?dsetInstance <http://ontodm.com/SemanticAnnotation#numOfDescriptiveFeatures> ?numDescriptive .\n"+
      "  ?dsetInstance <http://ontodm.com/SemanticAnnotation#numberOfInstances> ?numInstances . \n"+
      "  ?dsetInstance <http://ontodm.com/SemanticAnnotation#hasMissingValues> ?hasMissingValues . \n");

      if(this.mappings.length>0){
        queryL = queryL.concat(
          "{\n"+
          "  select (count (?mfInstance) as ?mf) ?dsetInstance\n"+
          "  where {\n"+
          "      ?dsetInstance <http://purl.obolibrary.org/obo/RO_0000086> ?mfInstance .\n"+
          "      ?mfInstance <http://www.ontodm.com/OntoDT#OntoDT_0000240> ?mfValue .\n"+
          "      ?mfInstance <http://ontodm.com/SemanticAnnotation#typeName> ?mfLabel .\n"+
          "      FILTER("+metaFeaturesStr+").\n"+
          "  }\n"+
          "  \n"+
          "  group by ?dsetInstance\n"+
          "}\n"+
          "filter (?mf = "+this.mappings.length+") .\n"
          );
      }

      if(this.selected4=='with missing'){
        queryL = queryL.concat(
        "  FILTER(?hasMissingValues=true)\n"
        );
      }
      else{
        if(this.selected4=='without missing'){
          queryL = queryL.concat(
          "  FILTER(?hasMissingValues=false)\n"
          );
        }
        else {
          queryL = queryL.concat(
            "  FILTER(?hasMissingValues in (false, true))\n"
            );
        }
      } 
      
      if(this.numberOfDescriptiveFeatures!=undefined){
        queryL = queryL.concat(
          " FILTER("+this.rangeFilter(this.numberOfDescriptiveFeatures, '?numDescriptive')+")\n"
          );
      }
      if(this.numberOfTargetFeatures!=undefined){
        queryL = queryL.concat(
          " FILTER("+this.rangeFilter(this.numberOfTargetFeatures, '?numTargets')+")\n"
          );
      }

      queryL = queryL.concat(
        "  ?dsInstance <http://purl.obolibrary.org/obo/IAO_0000136> ?dsetInstance .\n"+
        "  ?dsInstance rdf:type ?datasetClass .\n"+
        "  ?datasetClass rdfs:subClassOf <http://www.ontodm.com/OntoDM-core/OntoDM_400000> .\n"+
        "  ?datasetClass rdfs:subClassOf ?datasetSuperClass .\n"+
        "  ?datasetSuperClass rdfs:label ?datasetSuperClassLabel .\n"+
        "  FILTER( ?datasetSuperClassLabel IN ("+datasetSpecificationLabelString+")).\n"
        // "  ?dsInstance rdfs:label ?datasetLabel .\n"
      );
     
      if(isMeta){
        queryL = queryL.concat(
        "  ?dsetInstance <http://purl.obolibrary.org/obo/RO_0000086> ?mfInstance .\n"+
        "  ?mfInstance <http://www.ontodm.com/OntoDT#OntoDT_0000240> ?mfValue .\n"+
        "  ?mfInstance <http://ontodm.com/SemanticAnnotation#typeName> ?mfLabel .\n"
        )
      }
      queryL = queryL.concat(     
        "}\n"
      );
      return queryL;
  }

  requestedDescriprive = function(){
    return this.selectedDescriptiveFeatureSpec!=undefined &&
     this.numberOfDescriptiveFeatures!=undefined && this.numberOfDescriptiveFeatures!="";
  }

}