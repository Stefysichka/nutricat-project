import { Component, Input, Output, EventEmitter } from '@angular/core';
import { CommonModule } from '@angular/common';
import { CustomButtonComponent } from '../custom-button/custom-button.component';

@Component({
  selector: 'app-modal',
  imports: [CommonModule, CustomButtonComponent],
  templateUrl: './modal.component.html',
  styleUrl: './modal.component.scss'
})
export class ModalComponent {
  @Input() title: string = '';
  @Input() isOpen: boolean = false;
  
  @Input() confirmText: string = 'Ок';
  @Input() cancelText: string = "Скасувати";

  @Output() confirm = new EventEmitter<void>();
  @Output() close = new EventEmitter<void>

  onConfirm(){
    this.confirm.emit();
  }

  onClose(){
    this.close.emit()
  }
}
