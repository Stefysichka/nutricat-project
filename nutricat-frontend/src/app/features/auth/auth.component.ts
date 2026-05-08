import { Component, inject } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { Router } from '@angular/router';
import { AuthService } from '../../core/services/auth.service';
import { CustomButtonComponent } from '../../shared/components/custom-button/custom-button.component';

@Component({
  selector: 'app-auth',
  standalone: true,
  imports: [CommonModule, FormsModule, CustomButtonComponent],
  templateUrl: './auth.component.html',
  styleUrl: './auth.component.scss'
})
export class AuthComponent {
  private authService = inject(AuthService);
  private router = inject(Router);

  isLoginMode = true; 
  isLoading = false;
  errorMessage = '';

  
  formData = {
    username: '', 
    email: '',
    password: ''
  };

  toggleMode() {
    this.isLoginMode = !this.isLoginMode;
    this.errorMessage = '';
  }

  onSubmit() {
    if (!this.formData.email || !this.formData.password) {
      this.errorMessage = 'Заповніть всі обов\'язкові поля';
      return;
    }

    this.isLoading = true;
    this.errorMessage = '';

    if (this.isLoginMode) {
      
      this.authService.login({ email: this.formData.email, password: this.formData.password }).subscribe({
        next: () => {
          this.isLoading = false;
          this.router.navigate(['/cats']); 
        },
        error: (err) => {
          this.isLoading = false;
          this.errorMessage = 'Неправильний email або пароль';
          console.error(err);
        }
      });
    } else {
      
      this.authService.register(this.formData).subscribe({
        next: () => {
          
          this.authService.login({ email: this.formData.email, password: this.formData.password }).subscribe(() => {
            this.isLoading = false;
            this.router.navigate(['/cats']);
          });
        },
        error: (err) => {
          this.isLoading = false;
          this.errorMessage = 'Помилка реєстрації. Можливо, такий email вже існує.';
          console.error(err);
        }
      });
    }
  }
}