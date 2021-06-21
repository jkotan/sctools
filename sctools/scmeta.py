#!/usr/bin/env python
#   This file is part of sctools - Scientific Catalog Tools
#
#    Copyright (C) 2021-2021 DESY, Jan Kotanski <jkotan@mail.desy.de>
#
#    nexdatas is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    nexdatas is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with sctools.  If not, see <http://www.gnu.org/licenses/>.
#

""" Command-line tool for dumping creating scicat json config """

import sys
# import os
import simplejson as json
import argparse
# import argcomplete
import pprint


{
 "creationLocation": "/PSI/SLS/TOMCAT",
 "sourceFolder": "/scratch/devops",
 "type": "raw",
 "ownerGroup": "p16623"
}


def mdflatten(dct, keys, res):
    if isinstance(dct, dict):
        for ky, vl in dct.items():
            kys = list(keys)
            if isinstance(ky, str):
                kys.append(ky)
                mdflatten(vl, kys, res)
            else:
                key = ".".join(keys)
                # print("2.", key)
                res[key] = dct
                break

    else:
        key = ".".join(keys)
        # print("1.", key)
        res[key] = dct


class Loader(object):

    btmdmap = {
        "principalInvestigator": "pi.email",
        "pid": "beamtimeId",   # ?? is not unique for dataset
        "owner": "applicant.lastname",
        "contactEmail": "contact",
        "sourceFolder": "corePath",

        "endTime": "eventEnd",    # ?? or dataset
        "ownerEmail": "applicant.email",
        "description": "title",
        "createdAt": "generated",
        "updatedAt": "generated",
        "proposalId": "proposalId",
    }

    strcre = {
        "creationLocation": "/DESY/{facility}/{beamline}",
        "type": "raw",
    }

    cre = {
        "creationTime": [],  # ?? endTime for dataset !!!
        "ownerGroup": [],  # ??? !!!

        "sampleId": [],  # ???
        "publisheddateId": [],
        "accessGroups": [],  # ???
        "createdBy": [],  # ???
        "updatedBy": [],  # ???
        "createdAt": [],  # ???
        "updatedAt": [],  # ???
        "isPublished": ["false"],
        "dataFormat": [],
        "scientificMetadata": {},
        "orcidOfOwner": "ORCID of owner https://orcid.org if available",
        "sourceFolderHost": [],
        "size": [],
        "packedSize": [],
        "numberOfFiles": [],
        "numberOfFilesArchived": [],
        "validationStatus": [],
        "keywords": [],
        "datasetName": [],
        "classification": [],
        "license": [],
        "version": [],
        "techniques": [],
        "instrumentId": [],
        "history": [],
        "datasetlifecycle": [],

    }

    dr = {
        "eventStart": [],
        "beamlineAlias": [],
        "leader": [],
        "onlineAnalysis": [],
        "pi.*": [],
        "applicant.*": [],
        "proposalType": [],
        "users": [],
    }

    def __init__(self, options):
        """ loader constructor

        :param options: parser options
        :type options: :class:`argparse.Namespace`
        """
        self.__output = options.output
        dct = {}
        if options.beamtimemeta:
            with open(options.beamtimemeta, "r") as fl:
                # jstr = fl.read()
                # # print(jstr)
                dct = json.load(fl)
        self.__btmeta = dct
        dct = {}
        if options.scientificmeta:
            with open(options.scientificmeta, "r") as fl:
                jstr = fl.read()
                print(jstr)
                try:
                    dct = json.loads(jstr)
                except Exception:
                    if jstr:
                        nan = float('nan')    # noqa: F841
                        dct = eval(jstr)
                        # mdflatten(dstr, [], dct)
        self.__scmeta = dct
        # print("BEAMTIME:", self.__btmeta)
        # print("OUTPUT:", self.__output)
        self.__metadata = {}

    def run(self):
        """ the main program function

        :param options: parser options
        :type options: :class:`argparse.Namespace`
        :returns: output information
        :rtype: :obj:`str`
        """

        if self.__btmeta:
            for sc, ds in self.btmdmap.items():
                sds = ds.split(".")
                md = self.__btmeta
                for sd in sds:
                    if sd in md:
                        md = md[sd]
                    else:
                        print("%s cannot be found" % ds)
                        break
                else:
                    self.__metadata[sc] = md
            for sc, vl in self.strcre.items():
                self.__metadata[sc] = vl.format(**self.__btmeta)
        if self.__scmeta:
            self.__metadata["scientificMetadata"] = self.__scmeta
        pp = pprint.PrettyPrinter()
        pp.pprint(self.__metadata)
        # print(self.__metadata)
        if self.__output:
            with open(self.__output, "w") as fl:
                # jstr = fl.read()
                # # print(jstr)
                json.dump(self.__metadata, fl, indent=4)


def main():
    """ the main program function
    """

    #: pipe arguments
    # pipe = []
    # if not sys.stdin.isatty():
    #     #: system pipe
    #     pipe = sys.stdin.readlines()

    description = "Command-line tool for creating SciCat"

    epilog = "" \
        " examples:\n" \
        "       scmeta -b /tmp/metadata-beamtime-1234567.json " \
        "-o scicat-config.json \n" \
        "\n"
    parser = argparse.ArgumentParser(
        description=description, epilog=epilog,
        formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("-b", "--beamtime-meta", dest="beamtimemeta",
                        help=("beamtime metadata file"))
    parser.add_argument("-s", "--scientific-meta", dest="scientificmeta",
                        help=("beamtime metadata file"))
    parser.add_argument("-o", "--output", dest="output",
                        help=("output scicat metadata file"))
    try:
        options = parser.parse_args()
    except Exception as e:
        sys.stderr.write("Error: %s\n" % str(e))
        sys.stderr.flush()
        parser.print_help()
        print("")
        sys.exit(255)

    try:
        result = Loader(options).run()

        # except PyTango.DevFailed as
    except Exception as e:
        sys.stderr.write("Error: %s. \n" % str(e))
        sys.stderr.flush()
        sys.exit(255)
    if result and str(result).strip():
        print(result)
    sys.exit(0)


if __name__ == "__main__":
    main()
