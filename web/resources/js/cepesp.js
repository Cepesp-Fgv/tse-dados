import axios from 'axios';

async function getQuery(params) {
    let response = await axios.get('/api/consulta/athena/query', {
        params,
        paramsSerializer: (p) => $.param(p),
    });

    return {
        id: response.data.id,
        sql: response.data.sql,
        name: response.data.name,
        table: params.table,
        start: params.start,
        length: params.length
    };
}

async function getStatus(query_id) {
    let params = {id: query_id};
    let response = await axios.get('/api/consulta/athena/status', {params});
    let {status, message} = response.data;

    return [status, message];
}

async function getResult(query_id, start, length, format) {
    let params = {
        id: query_id,
        start: start,
        length: length,
        format: format || 'json',
        ignore_version: true
    };
    let response = await axios.get('/api/consulta/athena/result', {params});

    return response.data;
}

async function getColumns(params) {
    let response = await axios.get('/api/consulta/athena/columns', {
        params,
        paramsSerializer: (p) => $.param(p),
    });

    return {
        'columns': response.data.columns || [],
        'translated_columns': response.data.translated_columns || {},
        'default_columns': response.data.default_columns || [],
        'descriptions': response.data.descriptions || {},
    }
}


async function runQuery(params, onStatusUpdateCallback, sleepDelay) {
    let info = await startQuery(params, onStatusUpdateCallback, sleepDelay);
    let results = await getResult(info.id, info.start, info.length, params.format);
    return {info, results};
}


async function startQuery(params, onStatusUpdateCallback, sleepDelay) {
    let info = await getQuery(params);
    let status = "QUEUED";
    let message = "";
    let sleep = sleepDelay || 1000;
    let total = 0;

    while (status === "RUNNING" || status === "QUEUED") {
        if (onStatusUpdateCallback) onStatusUpdateCallback(status, message, total);

        await wait(sleep); total += sleep;

        let [newStatus, newMessage] = await getStatus(info.id);
        status = newStatus;
        message = newMessage;
    }

    if (onStatusUpdateCallback) onStatusUpdateCallback(status, message, total);

    return info;
}


async function lambdaQuery(params) {
    let response = await axios.get('https://api.cepespdata.io/api/query/result', {
        params,
        paramsSerializer: (p) => $.param(p),
    });

    return response.data;
}


function getYears(job) {
    switch (parseInt(job)) {
        case 1:
        case 2:
        case 3:
        case 4:
        case 5:
        case 6:
        case 7:
        case 8:
        case 9:
        case 10:
            return [2018, 2014, 2010, 2006, 2002, 1998];
        case 11:
        case 12:
        case 13:
            return [2016, 2012, 2008, 2004, 2000];
        default:
            return [];
    }
}

export default {getQuery, getStatus, getResult, getYears, getColumns, runQuery, startQuery, lambdaQuery};