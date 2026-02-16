import { Component, Input, Output, EventEmitter } from '@angular/core';
import {RouterLink, RouterLinkActive} from '@angular/router';
import { CommonModule } from '@angular/common';
import { NavLink } from '../../../domain/models/nav-link.model';
import { User } from '../../../domain/models/user.module';

@Component({
  selector: 'app-navbar',
  imports: [CommonModule, RouterLink, RouterLinkActive],
  templateUrl: './navbar.component.html',
  styleUrl: './navbar.component.scss'
})
export class NavbarComponent {
  @Input() links: NavLink[] = [];
  @Input() user?: User;

  @Output() logout = new EventEmitter<void>();

  onLogout(){
    this.logout.emit();
  }
}
