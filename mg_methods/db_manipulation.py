from os import listdir
import pandas as pd
from sqlalchemy import text as sql_text
import time
from datetime import datetime
from pandas import to_datetime


class mugas_DB_functions:

    def __init__(self, engine):
        self.sqlEngine = engine

    def get_sql_request(self, sqlQ):
        status = 'error'
        response = []
        try:
            self.sqlEngine.dispose()
            con = self.sqlEngine.connect()
            response = read_sql(sql_text(sqlQ), con).to_dict(orient='records')
            status = 'success'
        except:
            pass
        con.close()
        return {'status': status, 'response': response}

    def get_all_tables(self):
        self.sqlEngine.dispose()
        con = self.sqlEngine.connect()
        response = pd.read_sql(sql_text('SHOW TABLES'),
                               con).to_dict(orient='records')
        con.close()
        return {'status': 'success', 'response': response}

    def delete_record(self, db_table_name, filterDict):
        filterStrLst = [
            fltcol+'="{}"'.format(filterDict[fltcol]) for fltcol in [*filterDict]]
        filterStr = ' AND '.join(filterStrLst)
        self.sqlEngine.dispose()
        con = self.sqlEngine.connect()
        sqlQuery = "DELETE FROM {} WHERE {}".format(db_table_name, filterStr)
        con.execute(sql_text(sqlQuery))
        con.close()
        return {'status': 'Table {} updated successfully'.format(db_table_name), 'response': []}

    def get_all_records_between_ranges(self, db_table_name, returnCols, colName, startVal, endVal):
        status = 'error'
        response = {'status': 'error', 'response': []}
        try:
            self.sqlEngine.dispose()
            con = self.sqlEngine.connect()
            sql_q = "SELECT {} FROM {} WHERE {} BETWEEN {} AND {}"
            response = {'status': 'success', 'response': pd.read_sql(sql_text(sql_q.format(','.join(
                returnCols), db_table_name, colName, startVal, endVal)), con).to_dict(orient='records')}
        except:
            pass
        con.close()
        return response

    def get_filtered_records_between_ranges(self, parameters):
        db_table_name = parameters["db_table_name"]
        returnCols = parameters["returnColumns"]
        filterDict = parameters["filterDict"]
        colName = parameters["colName"]
        startVal = parameters["startVal"]
        endVal = parameters["endVal"]
        filterPairs = [ky+'={}'.format(filterDict[ky]) for ky in [*filterDict]]
        response = {'status': 'error', 'response': []}
        try:
            self.sqlEngine.dispose()
            con = self.sqlEngine.connect()
            sql_q = "SELECT {} FROM {} WHERE {} BETWEEN {} AND {} AND {}"
            sqlQ = sql_q.format(','.join(returnCols), db_table_name,
                                colName, startVal, endVal, ' AND '.join(filterPairs))
            # print(sqlQ)
            response = {'status': 'success', 'response': pd.read_sql(
                sql_text(sqlQ), con).to_dict(orient='records')}
        except:
            pass
        con.close()
        return response

    def get_all_records_column_values_in(self, db_table_name, returnCols, colName, colVals):
        response = {'status': 'error', 'response': []}
        try:
            self.sqlEngine.dispose()
            con = self.sqlEngine.connect()
            sql_q = "SELECT {} FROM {} WHERE {} IN ({})"
            response = {'status': 'success', 'response': pd.read_sql(sql_text(sql_q.format(','.join(
                returnCols), db_table_name, colName, ', '.join([str(xx) for xx in colVals]))), con).to_dict(orient='records')}
        except:
            pass
        con.close()
        return response

    def get_filtered_records_column_values_in(self, db_table_name, returnCols, filterDict, colName, colVals):
        response = {'status': 'error', 'response': []}
        try:
            filterPairs = [ky+'="{}"'.format(filterDict[ky])
                           for ky in [*filterDict]]
            self.sqlEngine.dispose()
            con = self.sqlEngine.connect()
            sql_q = "SELECT {} FROM {} WHERE {} IN ({}) AND {}"
            response = {'status': 'success', 'response': pd.read_sql(sql_text(sql_q.format(','.join(returnCols), db_table_name, colName, ', '.join([
                                                                     str(xx) for xx in colVals]), ' AND '.join(filterPairs))), con).to_dict(orient='records')}
        except:
            pass
        con.close()
        return response

    def insert_record(self, params):
        msg = 'error'
        try:
            db_table_name = params['db_table_name']
            updateDict = params['updateDict']
            self.sqlEngine.dispose()
            con = self.sqlEngine.connect()
            db_table_PDF = pd.read_sql(sql_text(
                'SELECT * FROM {} WHERE id=(SELECT max(id) FROM {})'.format(db_table_name, db_table_name)), con)
            diffCols = set([*updateDict]).difference(set([*db_table_PDF]))
            if len(diffCols) == 0:
                lastIndex = db_table_PDF['id'].values[0]
                insert_entry_PDF = pd.DataFrame(
                    columns=[*db_table_PDF], index=[int(lastIndex+1)]).drop(columns=['id'])
                insert_entry_PDF.loc[int(
                    lastIndex+1), [*updateDict]] = [updateDict[ky] for ky in [*updateDict]]
                insert_entry_PDF.to_sql(
                    db_table_name, con, if_exists='append', index=True, index_label='id')
                msg = 'Table {} updated successfully'.format(db_table_name)
            else:
                msg = 'Insert columns'+', '.join(diffCols)+' not in table'
        except:
            pass
        con.close()
        return msg

    def update_table_records_simple(self, tablename, recordid, updatedict, timestampsdict):
        '''
        Webserice call: {"moduleid":<module id>, "updatedict":<dict of key value pairs to be updated>}
        Response: {'status':status,'response':response}
        '''
        response = []
        status = "error"
        try:
            keyvals = ', '.join(['{}={}'.format(ky, updatedict[ky])
                                for ky in [*updatedict]])
            if len(timestampsdict) != 0:
                keyvals = keyvals+', '+', '.join(['{}={}'.format(ky, int(time.mktime(to_datetime(timestampsdict[ky], errors='raise',
                                                 dayfirst=True, infer_datetime_format=True).to_pydatetime().timetuple()))) for ky in [*timestampsdict]])
            self.sqlEngine.dispose()
            con = self.sqlEngine.connect()
            sqlQ = 'UPDATE {} SET {} WHERE id={}'.format(
                tablename, keyvals, recordid)
            con.execute(sql_text(sqlQ))
            status = 'success'
        except:
            pass

        con.close()
        return {'status': status, 'response': response}

    def update_record(db_table_name, filterDict, updateStrDict, updateNumericDict, updateTimeStrDict):
        '''
        Pass text filter strings as '"\text\"' and time strings with day first
        '''
        filterStrLst = [
            fltcol+'={}'.format(filterDict[fltcol]) for fltcol in [*filterDict]]
        filterStr = ' AND '.join(filterStrLst)
        setText = ''
        if len(updateTimeStrDict) != 0:
            setText = ', '.join(['{}={}'.format(ky, int(time.mktime(to_datetime(updateTimeStrDict[ky], errors='raise',
                                dayfirst=True, infer_datetime_format=True).to_pydatetime().timetuple()))) for ky in [*updateTimeStrDict]])
        if len(updateStrDict) != 0:
            if setText != '':
                setText = setText+', '
            setText = setText + \
                ', '.join([xx+"='{}'".format(updateStrDict[xx].replace('\\', '\\\\'))
                          for xx in [*updateStrDict]])
        if len(updateNumericDict) != 0:
            if setText != '':
                setText = setText+', '
            setText = setText + \
                ', '.join([xx+"={}".format(updateNumericDict[xx])
                          for xx in [*updateNumericDict]])
        self.sqlEngine.dispose()
        con = self.sqlEngine.connect()
        sqlQ = "UPDATE {} SET {} WHERE {}".format(
            db_table_name, setText, filterStr)
        con.execute(sql_text(sqlQ))
        con.close()
        return {'status': 'SQL querry: {} executed successfully'.format(sqlQ), 'response': []}

    def bulk_update_table_entries_with_logging(self, params):
        filterCols = params['filterCols']
        updateDataDictList = params['updateDictList']
        filterDict = {}
        for dct in updateDataDictList:
            filterDict = {ky: dct[ky] for ky in filterCols}
            msg = self.update_record(
                {'db_table_name': params['db_table_name'], 'filterDict': filterDict, 'updateDict': dct})
            dct[params['db_table_name']+'_updated_by'] = params['updatedBy']
            dct[params['db_table_name']+'_update_comment'] = params['updateComment']
            dct[params['db_table_name'] +
                '_updated_on'] = datetime.now().strftime('%Y/%m/%d %H:%M:%S')
            msg = self.insert_record(
                {'db_table_name': params['db_table_name']+'_update_history', 'updateDict': dct})
        return msg

    def bulk_delete_table_entries_with_logging(self, params):
        deleteDataDictList = params['updateDictList']
        filterDict = {}
        for dct in deleteDataDictList:
            msg = self.delete_record(
                {'db_table_name': params['db_table_name'], 'filterDict': dct})
            dct[params['db_table_name']+'_updated_by'] = params['updatedBy']
            dct[params['db_table_name']+'_update_comment'] = params['updateComment']
            dct[params['db_table_name'] +
                '_updated_on'] = datetime.now().strftime('%Y/%m/%d %H:%M:%S')
            msg = self.insert_record(
                {'db_table_name': params['db_table_name']+'_update_history', 'updateDict': dct})
        return msg

    def bulk_insert_table_entries_with_logging(self, params):
        updateDataDictList = params['updateDictList']
        for dct in updateDataDictList:
            msg = self.insert_record(
                {'db_table_name': params['db_table_name'], 'updateDict': dct})
            dct[params['db_table_name']+'_updated_by'] = params['updatedBy']
            dct[params['db_table_name']+'_update_comment'] = params['updateComment']
            dct[params['db_table_name'] +
                '_updated_on'] = datetime.now().strftime('%Y/%m/%d %H:%M:%S')
            msg = self.insert_record(
                {'db_table_name': params['db_table_name']+'_update_history', 'updateDict': dct})
        return msg

    def create_table_4m_csv_with_update_history(self, params):
        dataPDF = pd.read_csv(params['filePath'])
        tableName = params['db_table_name']
        self.sqlEngine.dispose()
        con = self.sqlEngine.connect()
        dataPDF.to_sql(tableName, con, if_exists='replace',
                       index=True, index_label=tableName+'_id')
        dataPDF[tableName+'_update_comment'] = 'Entry created'
        dataPDF.to_sql(tableName+'_update_history', con, if_exists='replace',
                       index=True, index_label=tableName+'_update_history_id')
        con.close()
        return 'Tables {} and {} Created'.format(tableName, tableName+'_update_history')

    def create_table_4m_csv(self, params):
        dataPDF = pd.read_csv(params['filePath'])
        tableName = params['db_table_name']
        self.sqlEngine.dispose()
        con = self.sqlEngine.connect()
        dataPDF.to_sql(tableName, con, if_exists='replace',
                       index=True, index_label=tableName+'_id')
        con.close()
        return 'Tables {} Created'.format(tableName)

    def create_DB_from_csv_directory(self, params):
        historyTablesPath = params['withHistoryTablesPath']
        tablesWithoutHistoryPath = params['withoutHistoryTablesPath']
        tableNamesWithHistory = listdir(historyTablesPath)
        tableNamesWithoutHistory = listdir(tablesWithoutHistoryPath)
        for flnm in tableNamesWithHistory:
            tableName = flnm.split('.')[0]
            self.create_table_4m_csv_with_update_history(
                {'db_table_name': tableName, 'filePath': historyTablesPath+flnm})

        self.sqlEngine.dispose()
        con = self.sqlEngine.connect()
        for flnm in tableNamesWithoutHistory:
            dataPDF = pd.read_csv(tablesWithoutHistoryPath+flnm)
            tableName = flnm.split('.')[0]
            dataPDF.to_sql(tableName, con, if_exists='replace',
                           index=True, index_label=tableName+'_id')
        con.close()
        return 'DB Created'
