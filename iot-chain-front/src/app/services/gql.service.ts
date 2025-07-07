import { Injectable } from "@angular/core";
import { ApolloClient, InMemoryCache, createHttpLink } from "@apollo/client/core";
import { setContext } from "@apollo/client/link/context";
import { environment } from "../../environments/environment";
import { gql } from "@apollo/client/core";
import { DeviceModel } from "../models/devices";

@Injectable({
  providedIn: 'root',
})
export class GraphQLService {
    private apolloClient: any;
    
    constructor() {
        const httpLink = createHttpLink({ uri: environment.apiUrl });
    
        const authLink = setContext(() => {
        const token = localStorage.getItem('token');
        return {
            headers: {
            Authorization: token ? `Bearer ${token}` : '',
            },
        };
        });
    
        this.apolloClient = new ApolloClient({
        link: authLink.concat(httpLink),
        cache: new InMemoryCache(),
        });
    }
    
    getApolloClient() {
        return this.apolloClient;
    }

    getDevices() {
        const DEVICES_QUERY = gql`
            query {
                devices {
                    id
                    name
                    description
                    mac
                    imei
                    deviceId
                }
            }
        `;

        return this.apolloClient.query({ query: DEVICES_QUERY });
    }

    addDevice(device: DeviceModel) {
        const ADD_DEVICE_MUTATION = gql`
            mutation AddDevice($device: DeviceInput!) {
                addDevice(device: $device) {
                    id
                    name
                    description
                    mac
                    imei
                    deviceId
                }
            }
        `;

        return this.apolloClient.mutate({
            mutation: ADD_DEVICE_MUTATION,
            variables: { device },
        });
    }

    updateDevice(device: DeviceModel) {
        const UPDATE_DEVICE_MUTATION = gql`
            mutation UpdateDevice($device: DeviceInput!) {
                updateDevice(device: $device) {
                    id
                    name
                    description
                    mac
                    imei
                    deviceId
                }
            }
        `;

        return this.apolloClient.mutate({
            mutation: UPDATE_DEVICE_MUTATION,
            variables: { device },
        });
    }

    deleteDevice(id: number) {
        const DELETE_DEVICE_MUTATION = gql`
            mutation DeleteDevice($id: ID!) {
                deleteDevice(id: $id) {
                    id
                }
            }
        `;

        return this.apolloClient.mutate({
            mutation: DELETE_DEVICE_MUTATION,
            variables: { id },
        });
    }

    getDeviceById(id: number) {
        const DEVICE_QUERY = gql`
            query GetDevice($id: ID!) {
                device(id: $id) {
                    id
                    name
                    description
                    mac
                    imei
                    deviceId
                }
            }
        `;

        return this.apolloClient.query({
            query: DEVICE_QUERY,
            variables: { id },
        });
    }

    getDevicesByUserId(userId: string) {
        const USER_DEVICES_QUERY = gql`
            query GetUserDevices($userId: ID!) {
                userDevices(userId: $userId) {
                    id
                    name
                    description
                    mac
                    imei
                    deviceId
                }
            }
        `;

        return this.apolloClient.query({
            query: USER_DEVICES_QUERY,
            variables: { userId },
        });
    }

    getUserDevices() {
        const USER_DEVICES_QUERY = gql`
            query {
                devices {
                    id
                    name
                }
            }
        `;

        return this.apolloClient.query({ query: USER_DEVICES_QUERY });
    }

    getDeviceData(id: number, dataFrom?: number, dataTo?: number) {
        const DEVICE_DATA_QUERY = gql`
            query GetDeviceData($id: Int!, $dataFrom: Int, $dataTo: Int) {
                deviceData(id: $id, dataFrom: $dataFrom, dataTo: $dataTo) {
                deviceId
                support
                mac
                imei
                sha256Orig
                timestamp
                data
                hash
                merkleProof
                txHash
                recordId
                tsCast
                date
                }
            }
        `;

        return this.apolloClient.query({
            query: DEVICE_DATA_QUERY,
            variables: { id, dataFrom, dataTo },
        });
    }

    getDeviceTime(id: number) {
        const DEVICE_TIME_QUERY = gql`
            query GetDeviceTime($id: Int!) {
                deviceTimes(id: $id) {
                    maxDate
                    minDate
                }
            }
        `;

        return this.apolloClient.query({
            query: DEVICE_TIME_QUERY,
            variables: { id },
        });
    }

}