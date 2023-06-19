import { BrowserModule } from '@angular/platform-browser';
import { NgModule } from '@angular/core';
import { NgMultiSelectDropDownModule } from 'ng-multiselect-dropdown';
import { FormsModule, ReactiveFormsModule } from '@angular/forms';
import { NgSelectModule } from '@ng-select/ng-select';
import { AppRoutingModule } from './app-routing.module';
import { AppComponent } from './app.component';
import { UiModule } from './ui/ui.module';
import { HttpClientModule}    from '@angular/common/http';
import { MaterialModule } from './material.module';
import { Ng4LoadingSpinnerModule } from 'ng4-loading-spinner';
import {NgbModule} from '@ng-bootstrap/ng-bootstrap';
import {BrowserAnimationsModule} from '@angular/platform-browser/animations';
import {MatCheckboxModule} from '@angular/material/checkbox';
import { SidebarModule } from 'ng-sidebar';
import {MatRadioModule} from '@angular/material/radio';
import {MatSidenavModule} from '@angular/material/sidenav';
import { TreeviewModule } from 'ngx-treeview';
import { DatasetComponent } from './dataset/dataset.component';
import {FilterComponent} from './filter/filter.component'
import { RouterModule, Routes } from '@angular/router';
import { DatasetsListComponent } from './datasets-list/datasets-list.component';
import { PlotlyModule } from 'angular-plotly.js';
import { GoogleChartsModule } from 'angular-google-charts';
import { HomeComponent } from './home/home.component';
import { LandingPageComponent } from './landing-page/landing-page.component';

@NgModule({
  declarations: [
    AppComponent,
    DatasetComponent,
    FilterComponent,
    DatasetsListComponent,
    HomeComponent,
    LandingPageComponent
  ],
  imports: [
    BrowserModule,
    AppRoutingModule,
    UiModule,
    HttpClientModule,
    FormsModule,
    ReactiveFormsModule,
    MaterialModule,
    NgSelectModule,
    Ng4LoadingSpinnerModule.forRoot(),
    NgMultiSelectDropDownModule.forRoot(),
    BrowserAnimationsModule,
    SidebarModule.forRoot(),
    NgbModule,
    MatCheckboxModule,
    MatRadioModule,
    MatSidenavModule,
    PlotlyModule,
    TreeviewModule.forRoot(),
    GoogleChartsModule.forRoot(),
  ],
  providers: [],
  bootstrap: [AppComponent]
})
export class AppModule { }
