import { Injectable, inject } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { BehaviorSubject, Observable, tap } from 'rxjs';
import { User } from '../../domain/models/user.module';

@Injectable({
  providedIn: 'root'
})
export class AuthService {
  private http = inject(HttpClient);
  private apiUrl = 'http://127.0.0.1:8000/api';


  private userSubject = new BehaviorSubject<User | undefined>(this.loadUserFromStorage());


  currentUser$ = this.userSubject.asObservable();


  private loadUserFromStorage(): User | undefined {
    const token = localStorage.getItem('access_token');
    const name = localStorage.getItem('user_name');
    if (token && name) {
      return { name: name } as User;
    }
    return undefined;
  }

  register(userData: any): Observable<any> {
    return this.http.post(`${this.apiUrl}/register/`, userData);
  }

  login(credentials: any): Observable<any> {
    const payload = { username: credentials.email, password: credentials.password };

    return this.http.post(`${this.apiUrl}/login/`, payload).pipe(
      tap((response: any) => {
        localStorage.setItem('access_token', response.access);
        localStorage.setItem('refresh_token', response.refresh);


        const userName = credentials.email.split('@')[0];
        localStorage.setItem('user_name', userName);
        this.userSubject.next({ name: userName } as User);
      })
    );
  }

  isLoggedIn(): boolean {
    return !!localStorage.getItem('access_token');
  }

  logout(): void {
    localStorage.removeItem('access_token');
    localStorage.removeItem('refresh_token');
    localStorage.removeItem('user_name');

    this.userSubject.next(undefined);
  }
}