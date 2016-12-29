import csv
import os
import threading
from atexit import register
from multiprocessing import Pool
from Queue import Queue
from random import randint
from functools import partial
from time import ctime
from uuid import uuid4
from zipfile import ZipFile, ZIP_DEFLATED
from lxml.etree import Element, ElementTree, fromstring


class ThreadXmlGenerator(threading.Thread):
    def __init__(self, queue):
        threading.Thread.__init__(self)
        self.queue = queue

    def run(self):
        index = self.queue.get()
        archive = ZipFile('archive_{}.zip'.format(index), 'a')
        for _ in range(1, 101):
            file_name = '{}.xml'.format(uuid4().hex)
            xml = self.generate_xml()
            xml.write(file_name)

            archive.write(file_name)
            os.remove(file_name)

        self.queue.task_done()

    @staticmethod
    def generate_xml():
        root = Element('root')

        root.append(Element('var', attrib={
            'name': 'id',
            'value': uuid4().hex
        }))

        root.append(Element('var', attrib={
            'name': 'level',
            'value': str(randint(1, 100))
        }))

        objects = Element('objects')
        for _ in range(randint(1, 10)):
            objects.append(Element('object', attrib={
                'name': uuid4().hex
            }))

        root.append(objects)
        return ElementTree(root)


def unwrap_self_f(arg, init):
    """
    We use the function outside the class
    to unpack the self from the argument
    and calls parse_archive again
    """
    return init.parse_archive(arg)


class Parser(object):
    """
    The parser generated documents in archives
    """

    @staticmethod
    def launch():
        with open('levels.csv', 'w') as fl_1, open('objects.csv', 'w') as fl_2:
            csv_1 = csv.writer(fl_1)
            csv_2 = csv.writer(fl_2)

            pool = Pool()
            zips = (os.path.join('./', f) for f in os.listdir('./') if 'zip' in f)

            f = partial(unwrap_self_f, init=Parser())
            for levels, objects in pool.map(f, zips):
                csv_1.writerows(levels)
                csv_2.writerows(objects)

            pool.close()
            pool.join()

    @staticmethod
    def parse_xml_elements(xml_data):

        root = fromstring(xml_data)
        id_ = root.xpath('./var[@name="id"]/@value')[0]
        level = root.xpath('./var[@name="level"]/@value')[0]

        objects = []
        for elem in root.xpath('objects/object'):
            objects.append((id_, elem.xpath('./@name')[0]))
        return (id_, level), objects

    def parse_archive(self, zip_path):
        archive = ZipFile(zip_path, 'r', ZIP_DEFLATED)
        levels, objects = [], []

        for file_name in archive.namelist():
            with archive.open(file_name) as fl_:
                content = fl_.read()

            file_level, file_obj = self.parse_xml_elements(content)

            levels.append(file_level)
            objects.extend(file_obj)
        return levels, objects


class Generator(object):
    """
    The generator of archives with xml documents
    """
    def __init__(self):
        self.archive_range = xrange(1, 51)

    def launch(self):
        queue = Queue()
        for _ in self.archive_range:
            ThreadXmlGenerator(queue).start()

        for index in self.archive_range:
            queue.put(index)

        queue.join()


def main():
    print 'Starting at {}'.format(ctime())

    Generator().launch()
    Parser.launch()


@register
def at_exit():
    print 'Finishing at {}'.format(ctime())


if __name__ == '__main__':
    main()
