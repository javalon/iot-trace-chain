import { CommonModule } from '@angular/common';
import { Component } from '@angular/core';
import { FormsModule } from '@angular/forms';
import { MatCardModule } from '@angular/material/card';
import { MatFormFieldModule } from '@angular/material/form-field';
import { MatInputModule } from '@angular/material/input';
import { MatButtonModule } from '@angular/material/button';
import { MatIconModule } from '@angular/material/icon';
import { MatTooltipModule } from '@angular/material/tooltip';
import { MatTableModule } from '@angular/material/table';
import { MatTableDataSource } from '@angular/material/table';
import { GraphQLService } from '../../services/gql.service';
import { DeviceModel } from '../../models/devices';
import { MatDialog, MatDialogModule, MAT_DIALOG_DATA, MatDialogRef } from '@angular/material/dialog';
import { Inject } from '@angular/core';
import { Component as DialogComponent } from '@angular/core';
import { MatSnackBar, MatSnackBarModule } from '@angular/material/snack-bar';
import { MatProgressSpinnerModule } from '@angular/material/progress-spinner';

@Component({
  selector: 'app-devices',
  imports: [
    CommonModule, 
    FormsModule, 
    MatCardModule,
     MatFormFieldModule,
     MatInputModule,
     MatButtonModule,
     MatIconModule,
     MatTooltipModule,
     MatTableModule,
     MatDialogModule,
     MatSnackBarModule,
     MatProgressSpinnerModule
  ],
  templateUrl: './devices.html',
  styleUrl: './devices.sass'
})
export class Devices {
  devices: DeviceModel[] = [];
  loading = true;
  error = '';

  selectedDevice: DeviceModel | null = null;
  isEditing = false;

  dataSource = new MatTableDataSource<any>();
  displayedColumns = ['name', 'description', 'mac', 'imei', 'deviceId', 'acciones'];

  constructor(
      @Inject(GraphQLService) private graphQLService: GraphQLService, 
      public dialog: MatDialog,
      private snackBar: MatSnackBar) 
    {
    this.fetchDevices();
  }

  fetchDevices() {
    this.graphQLService.getDevices()
      .then((result: any) => {
        this.devices = result.data.devices;
        this.dataSource.data = this.devices;
        this.loading = false;
      })
      .catch((err: any) => {
        console.error(err);
        this.error = 'Error al cargar dispositivos.';
        this.loading = false;
      });
  }

  addDevice(): void {
    const dialogRef = this.dialog.open(DeviceFormDialog, {
      data: {
        device: {
          id: null,
          name: '',
          description: '',
          mac: '',
          imei: '',
          deviceId: ''
        },
        isEditing: false
      }
    });

    dialogRef.afterClosed().subscribe(result => {
      if (result) {
        this.graphQLService.addDevice(result)
          .then(() => {
            this.snackBar.open('Dispositivo creado correctamente.', 'Cerrar', {
              duration: 3000,
            });
            this.fetchDevices()
          })
          .catch((err: any) => {
            console.error(err);
            this.error = 'Error al crear dispositivo.';
          });
      }
    });
  }

  editDevice(device: DeviceModel): void {
    const deviceCopy = { ...device };
    const dialogRef = this.dialog.open(DeviceFormDialog, {
      data: {
        device: deviceCopy,
        isEditing: true
      }
    });

    dialogRef.afterClosed().subscribe(result => {
      if (result) {
        this.graphQLService.updateDevice(result)
          .then(() => {
            this.snackBar.open('Dispositivo actualizado correctamente.', 'Cerrar', {
              duration: 3000,
            });
            this.fetchDevices()
          })
          .catch((err: any) => {
            console.error(err);
            this.error = 'Error al actualizar dispositivo.';
          });
      }
    });
  }

  removeDevice(device: DeviceModel) {
    if (!device || !device.id) return;

    const dialogRef = this.dialog.open(ConfirmDialog, {
      data: {
        title: '¿Eliminar dispositivo?',
        message: `¿Estás seguro de que quieres eliminar "${device.name}"?`
      }
    });

    dialogRef.afterClosed().subscribe(result => {
      if (result && device.id) {
        this.graphQLService.deleteDevice(device.id)
          .then(() => {
            this.snackBar.open('Dispositivo eliminado correctamente.', 'Cerrar', {
              duration: 3000,
            });
            this.fetchDevices();
          })
          .catch((err: any) => {
            console.error(err);
            this.error = 'Error al eliminar dispositivo.';
          });
      }
    });
  }

  saveDevice() {
    const dialogRef = this.dialog.open(ConfirmDialog, {
      data: {
        title: this.isEditing ? '¿Actualizar dispositivo?' : '¿Crear dispositivo?',
        message: this.isEditing
          ? `¿Deseas guardar los cambios en "${this.selectedDevice?.name}"?`
          : '¿Deseas crear este nuevo dispositivo?'
      }
    });

    dialogRef.afterClosed().subscribe(result => {
      if (!result) return;

      if (this.isEditing) {
        console.log('Guardando cambios de dispositivo:', this.selectedDevice);
        if (this.selectedDevice) {
          this.graphQLService.updateDevice(this.selectedDevice)
            .then(() => this.fetchDevices())
            .catch((err: any) => {
              console.error(err);
              this.error = 'Error al actualizar dispositivo.';
            });
        }
      } else {
        console.log('Creando nuevo dispositivo:', this.selectedDevice);
        if (this.selectedDevice) {
          this.graphQLService.addDevice(this.selectedDevice)
            .then(() => this.fetchDevices())
            .catch((err: any) => {
              console.error(err);
              this.error = 'Error al crear dispositivo.';
            });
        }
      }

      this.selectedDevice = null;
      this.isEditing = false;
    });
  }

  cancelEdit() {
    this.selectedDevice = null;
    this.isEditing = false;
  }

  formatearDeviceId(id: string): string {
    if (!id || id.length <= 10) return id;
    return `${id.substring(0, 5)}...${id.substring(id.length - 5)}`;
  }

  async actualizarDeviceId() {
    const mac = this.selectedDevice?.mac || '';
    const imei = this.selectedDevice?.imei || '';
    const data = mac + imei;

    if (!data) {
      if (this.selectedDevice) {
        this.selectedDevice.deviceId = '';
      }
      return;
    }

    const hash = await this.sha256(data);
    if (this.selectedDevice) {
      this.selectedDevice.deviceId = hash;
    }
  }

  private async sha256(message: string): Promise<string> {
    const msgBuffer = new TextEncoder().encode(message);
    const hashBuffer = await crypto.subtle.digest('SHA-256', msgBuffer);
    const hashArray = Array.from(new Uint8Array(hashBuffer));
    return hashArray.map(b => b.toString(16).padStart(2, '0')).join('');
  }

  async actualizarMac(valor: string) {
    const cleaned = valor.replace(/[^a-fA-F0-9]/g, '').toUpperCase();
    const macFormatted = cleaned.match(/.{1,2}/g)?.join(':').substring(0, 17) || '';
    if (this.selectedDevice) {
      this.selectedDevice.mac = macFormatted;
      this.actualizarDeviceId();
    }
  }
  
}

@DialogComponent({
  selector: 'confirm-dialog',
  template: `
    <h2 mat-dialog-title>{{ data.title }}</h2>
    <mat-dialog-content>{{ data.message }}</mat-dialog-content>
    <mat-dialog-actions align="end">
      <button mat-button mat-dialog-close [mat-dialog-close]="false">Cancelar</button>
      <button mat-button color="warn" [mat-dialog-close]="true">Confirmar</button>
    </mat-dialog-actions>
  `,
  standalone: true,
  imports: [MatDialogModule, MatButtonModule]
})
export class ConfirmDialog {
  constructor(@Inject(MAT_DIALOG_DATA) public data: { title: string; message: string }) {}
}

@DialogComponent({
  selector: 'device-form-dialog',
  template: `
    <h2 mat-dialog-title>{{ data.isEditing ? 'Editar Dispositivo' : 'Nuevo Dispositivo' }}</h2>
    <form (ngSubmit)="onSubmit()" #deviceForm="ngForm" style="display: flex; flex-direction: column; gap: 16px; padding: 0 24px 24px;">
      <mat-form-field appearance="fill">
        <mat-label>Nombre</mat-label>
        <input matInput type="text" [(ngModel)]="data.device.name" name="name" required #name="ngModel" />
        <mat-error *ngIf="name.invalid && name.touched">El nombre es obligatorio.</mat-error>
      </mat-form-field>

      <mat-form-field appearance="fill">
        <mat-label>Descripción</mat-label>
        <input matInput type="text" [(ngModel)]="data.device.description" name="description" />
      </mat-form-field>

      <mat-form-field appearance="fill">
        <mat-label>MAC</mat-label>
        <input matInput type="text" [(ngModel)]="data.device.mac" name="mac" (ngModelChange)="actualizarMac($event)" required #mac="ngModel" />
        <mat-error *ngIf="mac.invalid && mac.touched">La MAC es obligatoria.</mat-error>
      </mat-form-field>

      <mat-form-field appearance="fill">
        <mat-label>IMEI</mat-label>
        <input matInput type="text" [(ngModel)]="data.device.imei" name="imei" pattern="[0-9]*" (ngModelChange)="actualizarDeviceId()" required #imei="ngModel" />
        <mat-error *ngIf="imei.invalid && imei.touched">El IMEI debe contener solo números.</mat-error>
      </mat-form-field>

      <mat-form-field appearance="fill">
        <mat-label>Device ID</mat-label>
        <input matInput type="text" [(ngModel)]="data.device.deviceId" name="deviceId" readonly />
      </mat-form-field>

      <div style="display: flex; justify-content: flex-end; gap: 8px;">
        <button mat-raised-button color="primary" type="submit" [disabled]="deviceForm.invalid">Guardar</button>
        <button mat-button type="button" (click)="dialogRef.close()">Cancelar</button>
      </div>
    </form>
  `,
  standalone: true,
  imports: [CommonModule, FormsModule, MatFormFieldModule, MatInputModule, MatButtonModule]
})
export class DeviceFormDialog {
  constructor(
    public dialogRef: MatDialogRef<DeviceFormDialog>,
    @Inject(MAT_DIALOG_DATA) public data: { device: any; isEditing: boolean }
  ) {}

  onSubmit(): void {
    this.dialogRef.close(this.data.device);
  }

  async actualizarDeviceId() {
    const mac = this.data.device?.mac || '';
    const imei = this.data.device?.imei || '';
    const input = mac + imei;

    if (!input) {
      this.data.device.deviceId = '';
      return;
    }

    const encoder = new TextEncoder();
    const data = encoder.encode(input);
    const hashBuffer = await crypto.subtle.digest('SHA-256', data);
    const hashArray = Array.from(new Uint8Array(hashBuffer));
    const hashHex = hashArray.map(b => b.toString(16).padStart(2, '0')).join('');
    this.data.device.deviceId = hashHex;
  }

  async actualizarMac(valor: string) {
    const cleaned = valor.replace(/[^a-fA-F0-9]/g, '').toUpperCase();
    const macFormatted = cleaned.match(/.{1,2}/g)?.join(':').substring(0, 17) || '';
    this.data.device.mac = macFormatted;
    await this.actualizarDeviceId();
  }
}
