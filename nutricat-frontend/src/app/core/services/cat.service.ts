import { Injectable, inject } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';

@Injectable({
  providedIn: 'root'
})
export class CatService {
  private http = inject(HttpClient);
  
  
  private apiUrl = 'http://127.0.0.1:8000/api'; 

  sendChatMessage(messages: any[], catId?: string) {
    
    const payload = catId ? { messages, cat_id: catId } : { messages };
    return this.http.post(`${this.apiUrl}/chat/`, payload);
  }
  
  getCats(): Observable<any[]> {
    return this.http.get<any[]>(`${this.apiUrl}/cats/`);
  }

  
  getCatById(id: string | null): Observable<any> {
    
    return this.http.get<any>(`${this.apiUrl}/cats/${id}/`);
  }
  
  
  uploadCatPhoto(id: string | null, file: File): Observable<any> {
    const formData = new FormData();
    formData.append('photo', file);
    
    return this.http.patch(`${this.apiUrl}/cats/${id}/`, formData);
  }

  
  updateCatPhoto(catId: string, base64Photo: string) {
    return this.http.patch(`${this.apiUrl}/cats/${catId}/photo/`, { photo_url: base64Photo });
  }

  
  deleteCat(catId: string) {
    return this.http.delete(`${this.apiUrl}/cats/${catId}/`);
  }
  generateIdealRation(catId: string | number): Observable<any> {
    return this.http.post(`${this.apiUrl}/cats/${catId}/generate-ration/`, {});
  }
}
