import { Component, Input, Output, EventEmitter} from '@angular/core';
import { CommonModule } from '@angular/common';

@Component({
  selector: 'app-custom-button',
  imports: [CommonModule],
  templateUrl: './custom-button.component.html',
  styleUrl: './custom-button.component.scss'
})
export class CustomButtonComponent {
 @Input() label?: string;
 @Input() type: 'button' | 'submit' = 'button';
 @Input() variant: 'primary' | 'dark' = 'primary';
  
 @Output() onClick = new EventEmitter<void>();

 handleClick(){
  this.onClick.emit();
 }
}
