import { NgModule } from '@angular/core';
import { Routes, RouterModule } from '@angular/router';
import { FilterComponent } from './filter/filter.component';
import { DatasetComponent } from './dataset/dataset.component';
import { AppComponent } from './app.component';
import { DatasetsListComponent } from './datasets-list/datasets-list.component';
import { HomeComponent } from './home/home.component';
import { LandingPageComponent } from './landing-page/landing-page.component';

const routes: Routes = [
    {
        path: '',
        redirectTo: '/home',
        pathMatch: 'full'
    },  
    {
        path: 'home',
        component: LandingPageComponent
    },
    {
        path: 'filter',
        component: FilterComponent
    },
    {
      path: 'dataset/:name',
      component: DatasetComponent
    },
    {
      path: 'datasets-list',
      component: DatasetsListComponent
    },
    {
      path: 'about',
      component: HomeComponent

    }
  ];

@NgModule({
  imports: [RouterModule.forRoot(routes)],
  exports: [RouterModule]
})
export class AppRoutingModule { }
