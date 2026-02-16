import { Routes } from '@angular/router';
import {HomeComponent} from './features/home/home.component';
import { CatsComponent } from './features/cats/cats.component';

export const routes: Routes = [
    {path: '', component: HomeComponent},
    {path: 'cats', component: CatsComponent},
    {path: '**', redirectTo: ''}
];
