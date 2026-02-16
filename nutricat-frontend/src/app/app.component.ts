import { Component } from '@angular/core';
import { RouterOutlet } from '@angular/router';
import { NavbarComponent } from './core/layout/navbar/navbar.component';
import { NavLink } from './domain/models/nav-link.model';
import { User } from './domain/models/user.module';

@Component({
  selector: 'app-root',
  imports: [RouterOutlet, NavbarComponent],
  templateUrl: './app.component.html',
  styleUrl: './app.component.scss'
})
export class AppComponent {
  currentUser: User | undefined = { id: 1, name: 'Stefaniia', email: 'test@test.com' };

  userLinks: NavLink[] = [
    { label: 'Головна', path: '/' },
    { label: 'Мої коти', path: '/cats' }
  ]

  guestLinks: NavLink[] = [];

  get currentLinks(): NavLink[]{
    return this.currentUser ? this.userLinks : this.guestLinks;
  }
  onLogout() {
    console.log('Вихід з акаунту...');
    this.currentUser = undefined; // Імітуємо вихід
  }
}
