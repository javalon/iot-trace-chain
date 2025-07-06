export class DeviceModel{
    id: number | null;
    name: string;
    description: string;
    mac: string;
    imei: string;
    deviceId: string;
    userId?: string;
    
    constructor(id: number, name: string, description: string, mac: string, imei: string, deviceId: string, userId?: string) {
        this.id = id;
        this.name = name;
        this.description = description;
        this.mac = mac;
        this.imei = imei;
        this.deviceId = deviceId;
        this.userId = userId;
    }
}