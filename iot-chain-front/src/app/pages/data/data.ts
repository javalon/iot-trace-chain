import { CommonModule } from '@angular/common';
import { Component, Inject, inject } from '@angular/core';
import { MatFormFieldModule } from '@angular/material/form-field';
import { MatSelectChange, MatSelectModule } from '@angular/material/select';
import { FormsModule } from '@angular/forms';
import { GraphQLService } from '../../services/gql.service';
import { MatTableModule } from '@angular/material/table';
import { MatDatepickerModule } from '@angular/material/datepicker'; 
import { MatSnackBarModule, MatSnackBar } from '@angular/material/snack-bar';
import { MAT_DATE_LOCALE } from '@angular/material/core';
import { MatIconModule } from '@angular/material/icon';
import { MatProgressSpinnerModule } from '@angular/material/progress-spinner';
import { MatExpansionModule } from '@angular/material/expansion';
import { MatButtonModule } from '@angular/material/button';
import { MatTooltipModule } from '@angular/material/tooltip';
import { Web3Service } from '../../services/web3.service';
import { MatInputModule } from '@angular/material/input';
import { TextFieldModule } from '@angular/cdk/text-field';
import { hexStringToUint8Array, MerkleProof, verify_inclusion } from '../../utils/merkleTree';
import { provideLuxonDateAdapter } from '@angular/material-luxon-adapter';

@Component({
  selector: 'app-data',
  imports: [
    CommonModule,
    MatFormFieldModule,
    MatSelectModule,
    FormsModule,
    MatTableModule,
    MatDatepickerModule,
    MatSnackBarModule,
    MatIconModule,
    MatProgressSpinnerModule,
    MatExpansionModule,
    MatButtonModule,
    MatTooltipModule,
    MatInputModule,
    TextFieldModule
  ],
  templateUrl: './data.html',
  styleUrl: './data.sass',
  providers: [
    provideLuxonDateAdapter(),
    { provide: MAT_DATE_LOCALE, useValue: 'es-ES' },
  ]
})
export class Data {
  selectedDeviceId: number | null = null;
  devices: { id: number, name: string }[] = [];
  deviceDataSource: Record<string, any>[] = [];
  selectedDateFrom: Date | undefined;
  selectedDateTo: Date | undefined;
  maxRangeDate: Date = new Date();
  minRangeDate: Date = new Date();
  displayedColumns: string[] = [];
  noDeviceData = false;
  dataLoading = false;
  error = '';
  deviceInfor = {
    imei: '',
    mac: '',
    deviceId: '',
    deviceIdShort: ''
  }
 private snackBar = inject(MatSnackBar);

  constructor(
    @Inject(GraphQLService) private graphQLService: GraphQLService,
    @Inject(Web3Service) private web3Service: Web3Service
  ) {
    
    this.fetchUserDevices();
  }

  fetchUserDevices() {
    this.dataLoading = true;
    this.graphQLService.getUserDevices()
      .then((result: any) => {
        this.devices = result.data.devices.map((device: any) => ({
          id: device.id,
          name: device.name
        }));
        this.dataLoading = false;
        this.snackBar.open('Dispositivos cargados correctamente. Seleccione uno para cargar los datos', 'Cerrar', { duration: 3000 });
      })
      .catch((err: any) => {
        console.error(err);
      });
  }

  onDeviceChange(event: MatSelectChange) {
    const selectedId = event.value;
    this.maxRangeDate = new Date();
    this.minRangeDate = new Date();
    this.selectedDateFrom = undefined;
    this.selectedDateTo = undefined;
    this.deviceDataSource = [];
    if (this.selectedDeviceId) {
      this.getDeviceTime(selectedId);
    }
  }

  onDateChange(): void {
    if (this.selectedDateFrom && this.selectedDateTo && this.selectedDateFrom > this.selectedDateTo) {
      this.selectedDateTo = this.selectedDateFrom;
      this.snackBar.open('La fecha de fin se ha ajustado para no ser anterior a la fecha de inicio.', 'Cerrar', {duration: 3000});
    }
  }

  refreshData() {
    if (this.selectedDeviceId && this.selectedDateFrom && this.selectedDateTo) {
      this.getDeviceData(this.selectedDeviceId, this.selectedDateFrom, this.selectedDateTo);
    }
  }

  exportToCSV() {
    if (!this.deviceDataSource || this.deviceDataSource.length === 0) {
      this.snackBar.open('No hay datos para exportar.', 'Cerrar', { duration: 3000 });
      return;
    }
    const headers = Object.keys(this.deviceDataSource[0]).join(',') + '\n';
    const csvContent = headers + this.deviceDataSource.map(row => {
      return Object.values(row).map(value =>
        typeof value === 'object' && value !== null
          ? `"${JSON.stringify(value).replace(/"/g, '""')}"`
          : `"${String(value).replace(/"/g, '""')}"`
      ).join(',');
    }).join('\n');

    const blob = new Blob([csvContent], { type: 'text/csv;charset=utf-8;' });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = `device_data_${this.selectedDeviceId}.csv`;
    a.click();
    URL.revokeObjectURL(url);
    this.snackBar.open('Datos exportados a CSV.', 'Cerrar', { duration: 3000 });
  }

  copyToClipboard(proof: any) {
    const text = JSON.stringify(proof, null, 2);
    navigator.clipboard.writeText(text);
    this.snackBar.open('Texto copiado al portapapeles.', 'Cerrar', { duration: 3000 });
  }

  verifyAllMerkle() {
    if (!this.deviceDataSource) return;
    (async () => {
      for (const element of this.deviceDataSource) {
        await this.verifyMerkle(element);
      }
      this.snackBar.open('Verificación de Merkle completada.', 'Cerrar', { duration: 3000 });
    })();
  }

  async verifyMerkle(element: any): Promise<boolean> {
      if (element.proofData && element.proofData.merkleProof) {
        const merkleRoot = await this.web3Service.getMerkleRoot(element.proofData.deviceId, element.proofData.recordId);
        if (!merkleRoot) {
          console.error('Merkle root not found for deviceId:', element.proofData.deviceId, 'recordId:', element.proofData.recordId);
          element.proofData.verified = false;
          return false;
        }
        element.proofData.merkleRoot = merkleRoot;
        const isValid = await this.merkleVerification(
          merkleRoot,
          element.proofData.hash,
          element.proofData.merkleProof
        );
        element.proofData.verified = isValid;
        return isValid;
      } else {
        element.proofData.verified = false;
        return false;
      }
  }

  private async merkleVerification(root: string, leafHash: string, proof: any): Promise<boolean> {
    let proofObject = MerkleProof.deserialize(proof);
    try{
      const leafHashBytes = hexStringToUint8Array(leafHash);
      const rootBytes = hexStringToUint8Array(root);
      verify_inclusion(leafHashBytes, rootBytes, proofObject);
      this.snackBar.open('Merkle proof verificado correctamente. El dato no ha sido alterado.', 'Cerrar', { duration: 3000 });
    } catch (error) {
      console.error('Error verifying Merkle proof:', error);
      this.snackBar.open('Error al verificar el Merkle proof. El dato podría haber sido alterado.', 'Cerrar', { duration: 3000 });
      return false;
    }
    return true;
  }

  private getDeviceData(deviceId: number, fromDate?: Date, toDate?: Date) {
    this.dataLoading = true;
    if (!fromDate || !toDate) {
      fromDate = this.minRangeDate;
      toDate = this.maxRangeDate;
    }
    return this.graphQLService.getDeviceData(deviceId, fromDate.getTime()/1000, toDate.getTime()/1000)
      .then((result: any) => {
        const rawData = result.data.deviceData;
        this.deviceInfor.imei = rawData[0]?.imei || '';
        this.deviceInfor.mac = rawData[0]?.mac || '';
        this.deviceInfor.deviceId = rawData[0]?.deviceId || '';
        this.deviceInfor.deviceIdShort = this.formatearDeviceId(rawData[0]?.deviceId) || '';
        const data = rawData.map((item: any) => {
          const parsed = { ...item.data };
            const rawTimestamp = parsed.timestamp;
            if (
              rawTimestamp !== undefined &&
              (!isNaN(rawTimestamp) || !isNaN(Number(rawTimestamp)))
            ) {
              const timestampValue = Number(rawTimestamp);
              parsed.timestamp_unix = timestampValue;
              parsed.timestamp = new Date(timestampValue * 1000).toLocaleString();
            }
          parsed.proofData = {
            merkleProof: JSON.parse(item.merkleProof),
            txHash: item.txHash,
            recordId: item.recordId,
            deviceId: item.deviceId,
            hash: item.hash,
            verified: null,
            merkleRoot: null
          }
          return parsed;
        });
        const sortedData = data.sort((a:any, b:any) => b.timestamp_unix - a.timestamp_unix).map((item: any) => {
            delete item.timestamp_unix;
            return item;
        });
        this.deviceDataSource = sortedData;
        this.updateColumns();
        this.dataLoading = false;
        this.snackBar.open('Datos del dispositivo cargados correctamente.', 'Cerrar', { duration: 3000 });
      })
      .catch((err: any) => {
        console.error(err);
      });
  }

  private getDeviceTime(deviceId: number) {
    this.dataLoading = true;
    return this.graphQLService.getDeviceTime(deviceId)
      .then((result: any) => {
        const deviceTime = result.data.deviceTimes;
        if (deviceTime) {
          // Device time data is expected to have min_date and max_date as Unix timestamps. Ex: {'max_date': 1748770658, 'min_date': 1748711366}
          const minDateRaw = deviceTime.minDate;
          const maxDateRaw = deviceTime.maxDate;

          if (typeof minDateRaw === 'number' && typeof maxDateRaw === 'number') {
            this.minRangeDate = new Date(minDateRaw * 1000);
            this.maxRangeDate = new Date(maxDateRaw * 1000);

            // Validar que las fechas no sean inválidas
            if (!isNaN(this.minRangeDate.getTime()) && !isNaN(this.maxRangeDate.getTime())) {
              this.selectedDateTo = new Date(this.maxRangeDate.getTime() - 24 * 60 * 60 * 1000);
              this.selectedDateFrom = this.maxRangeDate;
              this.getDeviceData(deviceId, this.selectedDateFrom, this.selectedDateTo);
              this.noDeviceData = false;
            }else{
              this.noDeviceData = true;
            }
          }else{
            this.noDeviceData = true;
          }
        } else {
          console.warn('No device time data available.');
          this.noDeviceData = true;
        }
        this.dataLoading = false;
      })
      .catch((err: any) => {
        console.error(err);
      });
  }

  private updateColumns() {
    if (this.deviceDataSource.length > 0) {
      this.displayedColumns = Object.keys(this.deviceDataSource[0]);
    } else {
      this.displayedColumns = [];
    }
  }

  private formatearDeviceId(id: string): string {
    if (!id || id.length <= 10) return id;
    return `${id.substring(0, 5)}...${id.substring(id.length - 5)}`;
  }

}
