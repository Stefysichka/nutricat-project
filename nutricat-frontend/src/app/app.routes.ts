import { Routes } from '@angular/router';
import {HomeComponent} from './features/home/home.component';
import { CatsComponent } from './features/cats/cats.component';
import { CatChatComponent } from './features/cats/cat-chat/cat-chat.component';
import { authGuard } from './core/guards/auth.guard';
import { AuthComponent } from './features/auth/auth.component';
import { CatComponent } from './features/cats/cat/cat.component';

export const routes: Routes = [
    {path: '', component: HomeComponent},
    { path: 'auth', component: AuthComponent },
    {path: 'cats', component: CatsComponent},
    { path: 'cats/:id', component: CatComponent },
     { path: 'chat-test', component: CatChatComponent },
    {path: '**', redirectTo: ''},
];
