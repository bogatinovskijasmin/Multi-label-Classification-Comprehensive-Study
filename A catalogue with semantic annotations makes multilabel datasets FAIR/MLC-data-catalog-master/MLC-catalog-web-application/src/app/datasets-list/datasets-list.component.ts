import { Component, OnInit, ViewChild } from '@angular/core';
import { ActivatedRoute } from '@angular/router';
import { Observable, of } from 'rxjs';
import { map } from 'rxjs/operators';
import { MatPaginator, MatTableDataSource, MatSort } from '@angular/material';
import {NgbModal} from '@ng-bootstrap/ng-bootstrap';
import {DataService} from '..//data.service';
import { Ng4LoadingSpinnerService } from 'ng4-loading-spinner';
import { Router } from '@angular/router';

@Component({
  selector: 'app-datasets-list',
  templateUrl: './datasets-list.component.html',
  styleUrls: ['./datasets-list.component.css']
})
export class DatasetsListComponent implements OnInit {
  state$: Observable<object>;
  @ViewChild(MatPaginator) paginator: MatPaginator;
  @ViewChild(MatSort) sort: MatSort;
  displayedColumns: string[] = ['datasetLabel', 'numInstances', 'numDescriptive', 'numTargets', 'hasMissingValues'];
  dataSource:any;
  query:any;
  metaQuery:any;
  dict: {} = {};
  mataFeaturesPlotData: any[];
  cntAllDatasets:number =0;
  cntResultsDatasets:number=0;
  pieChartData: any[] = [];
  MLCMode: boolean = false;
  fromFilter: boolean = false;
  mappings: any[] = [];


  dsNames: String [] = [];
  selectedMetaFeatures = [];
  dropdownSettings = {};
  metaFeaturesMLC: string []=["DefaultAccuracy", "TotalDistinctClasses", "UnseenInTrain", "RatioTrainToPower", "RatioTestToPower", "RatioTotalToPower", 
  "RatioUnseenToTest", "Attributes", "Distinct labelsets", "Instances", "Labels", "LxIxF", "Ratio of number of instances to the number of attributes",
   "Cardinality", "Density", "Maximal entropy of labels", "Mean of entropies of labels", "Minimal entropy of labels", "Standard deviation of label cardinality",
    "CVIR inter class", "Kurtosis cardinality", "Max IR inter class", "Max IR intra class", "Max IR per labelset", "Mean of IR inter class",
     "Mean of IR intra class", "Mean of IR per labelset", "Mean of standard deviation of IR intra class", "Proportion of maxim label combination (PMax)",
      "Proportion of unique label combination (PUniq)", "Skewness cardinality", "Average examples per labelset", "Bound", "Diversity", "Number of labelsets up to 10 examples",
       "Number of labelsets up to 2 examples", "Number of labelsets up to 50 examples", "Number of labelsets up to 5 examples", "Mean examples per labelset", 
       "Number of unconditionally dependent label pairs by chi-square test", "Proportion of distinct labelsets", "Ratio of number of labelsets up to 10 examples",
        "Ratio of number of labelsets up to 2 examples", "Ratio of number of labelsets up to 50 examples", "Ratio of number of labelsets up to 5 examples", 
        "Ratio of unconditionally dependent label pairs by chi-square test", "SCUMBLE", "Standard deviation of examples per labelset", "Number of unique labelsets",
        "Average absolute correlation between numeric attributes", "Average gain ratio", "Number of binary attributes", "Mean of entropies of nominal attributes", "Mean of kurtosis", 
        "Mean of mean of numeric attributes", "Mean of skewness of numeric attributes", "Mean of standard deviation of numeric attributes", "Number of nominal attributes",
         "Number of numeric attributes", "Proportion of binary attributes", "Proportion of nominal attributes", "Proportion of numeric attributes", "Proportion of numeric attributes with outliers"];
  
  constructor(private dataService: DataService, private activatedRoute: ActivatedRoute, private modalService: NgbModal,
    private spinnerService: Ng4LoadingSpinnerService, private router:Router) { }

  ngOnInit() {
    this.spinnerService.show();
    // console.log("list spinner shown")
    this.dropdownSettings = {
      singleSelection: false,
      itemsShowLimit: 7,
      allowSearchFilter: true,
      enableCheckAll: false
    };

    this.initFunction().subscribe(res=>{
      
    });

    // this.initFunction();
  //  this.initFunction().subscribe(res=>{
  //    this.spinnerService.hide();
  //  });   
    
  }

  setSelectedFeatures(mappings){
    var newArray = [];
    if(mappings.length==0){
      return ['Average examples per labelset', "Proportion of numeric attributes with outliers"];
    }
    else{
      mappings.forEach(mapping => {
        newArray.push(String(mapping.feature));
      });
    }
    return newArray;
  }

  initFunction():Observable<any>{
    const intiObservable = new Observable(observer =>{
      this.activatedRoute.paramMap.pipe(map(() => window.history.state)).subscribe(res =>{
        this.state$=res.query; 
        this.mappings=res.mappings;
        if(this.state$!=undefined){
          this.query = res.query;
          this.metaQuery = res.metaQuery;
          this.dataService.getResults(this.query).subscribe(res=>{
            this.dataSource = new MatTableDataSource(this.formatResArray(res));
            this.dataSource.paginator = this.paginator;
            this.dataSource.sort = this.sort; 
            this.countAllDatasets();
          })
          this.executeMetaQuery(this.metaQuery);
          this.fromFilter = true;
          this.state$=undefined;
             
        }
        else{
          this.query = this.getAllDatasetsQuery();
          this.dataService.getResults(this.query).subscribe(res=>{
            this.dataSource = new MatTableDataSource(this.formatResArray(res));
            this.dataSource.paginator = this.paginator;
            this.dataSource.sort = this.sort; 
          })
        } 
        
      });
    })
    return intiObservable;
  }

  getAllDatasetsQuery(){
    var queryDatasets = "";
    queryDatasets = queryDatasets.concat(
        "PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#> \n"+
        "PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>\n"+
        "PREFIX OntoDM: <http://www.ontodm.com/OntoDM-core/>\n"+
        "PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>\n"+
        "SELECT DISTINCT ?dsetInstance ?datasetLabel ?numTargets ?numDescriptive ?numInstances ?hasMissingValues\n"+
        "WHERE {\n"+
        "  ?dsetInstance rdf:type ?dsetClass .\n"+
        "  ?dsetClass rdfs:subClassOf <http://www.ontodm.com/OntoDM-core/OntoDM_000144> .\n"+
        "  ?dsetInstance rdfs:label ?datasetLabel .\n"+
        "  ?dsetInstance <http://ontodm.com/SemanticAnnotation#numOfTargets> ?numTargets .\n"+
        "  ?dsetInstance <http://ontodm.com/SemanticAnnotation#numOfDescriptiveFeatures> ?numDescriptive .\n"+
        "  ?dsetInstance <http://ontodm.com/SemanticAnnotation#numberOfInstances> ?numInstances . \n"+
        "  ?dsetInstance <http://ontodm.com/SemanticAnnotation#hasMissingValues> ?hasMissingValues . \n"+
        "  FILTER(?hasMissingValues in (false, true))\n"+
        "  ?dsInstance <http://purl.obolibrary.org/obo/IAO_0000136> ?dsetInstance .\n"+
        "  ?dsInstance rdf:type ?datasetClass .\n"+
        "  ?datasetClass rdfs:subClassOf <http://www.ontodm.com/OntoDM-core/OntoDM_400000> .\n"+
        "  ?datasetClass rdfs:subClassOf ?datasetSuperClass .\n"+
        "  ?datasetSuperClass rdfs:label ?datasetSuperClassLabel .\n"+
        "  FILTER( ?datasetSuperClassLabel IN ('data specification'@en)).\n"+
        "}\n"
    );
    return queryDatasets;
  }
  getCount(res){
    return parseInt(res.results.bindings[0].cnt.value);
  }
  countAllDatasets(){
    var queryCountAllDatasets = "PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>\n"+
    "PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>\n"+
    "SELECT (count(distinct ?dsetInstance) as ?cnt)\n"+
    "WHERE {\n"+
    "     ?dsetInstance rdf:type ?dsetClass .\n"+
    "     ?dsetClass rdfs:subClassOf <http://www.ontodm.com/OntoDM-core/OntoDM_000144> .\n"+
    "     ?dsInstance <http://purl.obolibrary.org/obo/IAO_0000136> ?dsetInstance .\n"+
    "}";
    // console.log("Count Datasets:")
    this.dataService.getResults(queryCountAllDatasets).subscribe(res => {
      this.cntAllDatasets = this.getCount(res);
      this.pieChartData = this.populatePieChartData();
      // console.log(this.pieChartData); 
      // console.log(this.cntAllDatasets);
      
    });
  }

  populateMetaFeaturesData(){
    var array = [];
    this.selectedMetaFeatures.forEach(metaFeature => {
      array.push(
        {
          x: this.dsNames,
          y: this.dict[metaFeature],
          mode: this.dict[metaFeature].length<4? 'lines+markers':'lines',
          type: 'scatter',
          name: metaFeature
        }
      )
    });
    // console.log("Data: "+JSON.stringify(array));
    return array;
  }
  populatePieChartData(){
    var array = [];
    // console.log("match: "+ this.cntResultsDatasets);
    // console.log("all: "+this.cntAllDatasets);
    array.push({
      values: [this.cntAllDatasets-this.cntResultsDatasets, this.cntResultsDatasets],
      labels: ['rest', 'match'],
      type: 'pie'
    })
    return array;
  }

  onItemSelect(item: any) {
    this.mataFeaturesPlotData = this.populateMetaFeaturesData();
    
  }
  onItemDeSelect(item: any){
    this.mataFeaturesPlotData = this.populateMetaFeaturesData();
  }
  onSelectAll(items: any) {
  }

  executeMetaQuery(metaQuery){
    console.log(this.mappings)
    this.selectedMetaFeatures = this.setSelectedFeatures(this.mappings);
    this.dataService.getResults(metaQuery).subscribe(res => { 
      this.metaFeaturesMLC.forEach(mf =>{
        this.dict[mf] = [];
      })
      var array = res["results"].bindings;
      if(array.length>0){
        array.forEach(element => {
          var datasetLabel = element.datasetLabel.value.split(":")[1].split("-MLC")[0];
          if(!this.dsNames.includes(datasetLabel)) this.dsNames.push(datasetLabel);
          var mfLabel = element.mfLabel.value;
          var mfValue = element.mfValue.value;
          // console.log(mfLabel);
          this.dict[mfLabel].push(parseFloat(mfValue));
        });
        this.mataFeaturesPlotData = this.populateMetaFeaturesData();
      }
     
    });
  }

  open(content:any) {
    this.modalService.open(content, {ariaLabelledBy: 'modal-basic-title'});
  }

  formatResArray = function (res) {
    var newArray = [];
    this.cntResultsDatasets= res.results.bindings.length;
    console.log("Count results");
    console.log(this.cntResultsDatasets);
    res.results.bindings.forEach(element => {
      newArray.push({
        datasetLabel: element.datasetLabel.value.split(":")[1].split("-MLC")[0],
        numInstances: element.numInstances.value,
        numTargets: element.numTargets.value,
        numDescriptive: element.numDescriptive.value,
        hasMissingValues: element.hasMissingValues.value,
        dsetInstance: element.dsetInstance.value
      })
      
    });
    this.spinnerService.hide();
    return newArray;
  }


  onInitLoadDatasets(){
    // ?dsetInstance <http://purl.obolibrary.org/obo/RO_0000086> ?mfInstance .
    // ?mfInstance <http://www.ontodm.com/OntoDT#OntoDT_0000240> ?mfValue .
    // ?mfInstance <http://ontodm.com/SemanticAnnotation#typeName> ?mfLabel .
    // filter ((?mfLabel = "NumOfTest" && xsd:integer(?mfValue) > 100) || (?mfLabel = "NumOfTotal" && xsd:integer(?mfValue) > 1000)) .
    this.query = this.query.concat(
      "PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>\n"+
      "PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>\n"+
      "PREFIX OntoDM: <http://www.ontodm.com/OntoDM-core/>\n"+
      "SELECT DISTINCT ?dsetInstance ?datasetLabel ?numTargets ?numDescriptive ?numInstances ?hasMissingValues\n"+
      "WHERE {\n"+
      "    ?dsetInstance rdf:type ?dsetClass .\n"+
      "    ?dsetClass rdfs:subClassOf <http://www.ontodm.com/OntoDM-core/OntoDM_000144> .\n"+
      "    ?dsetInstance rdfs:label ?datasetLabel .\n"+
      "    ?dsetInstance <http://ontodm.com/SemanticAnnotation#numOfTargets> ?numTargets .\n"+
      "    ?dsetInstance <http://ontodm.com/SemanticAnnotation#numOfDescriptiveFeatures> ?numDescriptive .\n"+ 
      "    ?dsetInstance <http://ontodm.com/SemanticAnnotation#numberOfInstances> ?numInstances .\n"+
      "    ?dsetInstance <http://ontodm.com/SemanticAnnotation#hasMissingValues> ?hasMissingValues . \n"+
      "}\n"
    );
    this.executeQuery();

  }

  executeQuery = function(){
    this.dataService.getResults(this.query).subscribe(res => {  
      this.dataSource = new MatTableDataSource(this.formatResArray(res));
      this.dataSource.paginator = this.paginator;
      this.dataSource.sort = this.sort; 
    });
  }

}




