import { Component, inject, OnInit } from '@angular/core';
import { RouterOutlet, Router } from '@angular/router';
import { NavbarComponent } from './core/layout/navbar/navbar.component'; 
import { AuthService } from './core/services/auth.service';
import { NavLink } from './domain/models/nav-link.model';
import { User } from './domain/models/user.module';

@Component({
  selector: 'app-root',
  standalone: true,
  imports: [RouterOutlet, NavbarComponent],
  templateUrl: './app.component.html',
  styleUrl: './app.component.scss'
})
export class AppComponent implements OnInit {
  private authService = inject(AuthService);
  private router = inject(Router);

  
  currentUser: User | undefined = undefined; 

  
  navLinks: NavLink[] = [
    { path: '/', label: 'Головна' },
    { path: '/cats', label: 'Мої коти' }
  ];

  ngOnInit() {
    
    this.authService.currentUser$.subscribe(user => {
      this.currentUser = user;
    });
  }

  
  handleLogout() {
    this.authService.logout();
    this.router.navigate(['/']); 
  }
}