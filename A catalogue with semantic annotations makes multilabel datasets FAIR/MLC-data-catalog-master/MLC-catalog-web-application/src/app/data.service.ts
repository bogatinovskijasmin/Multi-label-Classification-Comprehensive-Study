import { Injectable } from '@angular/core';
import { Observable, of } from 'rxjs';
import { HttpClient, HttpHeaders } from '@angular/common/http';

@Injectable({
  providedIn: 'root'
})
export class DataService {
  url = "http://semantichub.ijs.si/fuseki/MLC-datasets/query";
  constructor(private http: HttpClient) { 

  }

  getResults(query): Observable<any[]>{
    const httpOptions = { headers: new HttpHeaders({'Content-Type': 'application/x-www-form-urlencoded'})};
    return this.http.get<any[]>(this.url+"?query="+encodeURIComponent(query), httpOptions);
  }

  getResultsWithURL(query, url): Observable<any[]>{
    const httpOptions = { headers: new HttpHeaders({'Content-Type': 'application/x-www-form-urlencoded'})};
    return this.http.get<any[]>(url+"?query="+encodeURIComponent(query), httpOptions);
  }

  // getLabel(query): Observable<any[]>{
  //   const httpOptions = { headers: new HttpHeaders({'Content-Type': 'application/x-www-form-urlencoded'})};
  //   return this.http.get<any[]>(this.url+"?query="+encodeURIComponent(query), httpOptions);
  // }

}
