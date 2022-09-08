# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface

# MYSQL
import pymysql
from sshtunnel import SSHTunnelForwarder
from CS_TM_Parse.mysql_config_parsing_sergei import host, ssh_port, port, user, \
    ssh_user, password, ssh_password, db_name, local_host, ssh_ip

import logging

import datetime


class CsTmParsePipeline:
    SQL_TABLE_NAME = 'CSMONEY'

    def __init__(self):
        # CREATING SSH TUNNEL
        tunnel = SSHTunnelForwarder((ssh_ip, ssh_port), ssh_password=ssh_password, ssh_username=ssh_user,
                                    remote_bind_address=(local_host, port))
        tunnel.start()
        self.connection = pymysql.connect(host=host, user=user, passwd=password, port=tunnel.local_bind_port,
                                          database=db_name, cursorclass=pymysql.cursors.DictCursor)

        logging.info("SSH_TUNNEL_CONNECTION_HAS_BEEN_ESTABLISHED :-)")

        # CREATING SQL TABLE
        with self.connection.cursor() as cursor:
            create_table_query = f"CREATE TABLE IF NOT EXISTS `{self.SQL_TABLE_NAME}` (" \
                                 f"`id` INT UNSIGNED NOT NULL AUTO_INCREMENT PRIMARY KEY," \
                                 f" `fullName` VARCHAR(64) NOT NULL," \
                                 f" `quality` VARCHAR(6) NOT NULL," \
                                 f" `float` FLOAT(42) UNSIGNED NOT NULL," \
                                 f" `price` FLOAT(22) UNSIGNED NOT NULL," \
                                 f" `overprice` FLOAT(22)," \
                                 f" `assetID` VARCHAR(64) NOT NULL UNIQUE," \
                                 f" `siteID` VARCHAR(64) NOT NULL," \
                                 f" `HighDemand` VARCHAR(10) NOT NULL," \
                                 f" `tradeLock` VARCHAR(22)," \
                                 f" created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP," \
                                 f" updated_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP);"
            cursor.execute(create_table_query)

        logging.info("SQL_TABLE_HAS_BEEN_CREATED :-)")

    def process_item(self, item, spider):

        if item['tradeLock'] != 'None':
            item['tradeLock'] = datetime.datetime.fromtimestamp(int(item['tradeLock']) / 1e3).strftime("%D at %H:%S")

        if item['float'] == None:
            item['float'] = 2

        if item['overprice'] == None:
            item['overprice'] = 0

        # SQL cannot accept name with ' symbol
        if "'" in item['fullName']:
            item['fullName'] = item['fullName'].replace("'", " ")
        
        print(item)

        # INSERT into Table
        with self.connection.cursor() as cursor:
            insert_data_query = f"INSERT INTO `{self.SQL_TABLE_NAME}` " \
                                f"(`fullName`,`quality`, `float`, `price`, `overprice`,`assetID`,`siteID`,`HighDemand`,`tradeLock`) " \
                                f"VALUES ('{item['fullName']}', '{item['quality']}',{item['float']}, {item['price']}," \
                                f" {item['overprice']}, '{item['assetID']}', '{item['siteID']}','{item['HighDemand']}','{item['tradeLock']}')" \
                                f" ON DUPLICATE KEY UPDATE `HighDemand`='{item['HighDemand']}', `price`={item['price']}, `overprice`={item['overprice']}, `updated_at` = CURRENT_TIMESTAMP;"
            cursor.execute(insert_data_query)
            try:
                self.connection.commit()
            except Exception as err1:
                logging.error(f"INSERT Error!\n{err1}")

        return item