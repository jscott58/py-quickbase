.. py-quickbase - Python bindings for Intuit's QuickBase
   Copyright (C) 2012-2014 WesTower Communications
   Copyright (C) 2014-2015 MasTec
   
   This file is part of py-quickbase.
   
   py-quickbase is free software: you can redistribute it and/or
   modify it under the terms of the GNU Lesser General Public License
   as published by the Free Software Foundation, either version 3 of
   the License, or (at your option) any later version.
   
   This program is distributed in the hope that it will be useful, but
   WITHOUT ANY WARRANTY; without even the implied warranty of
   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
   Lesser General Public License for more details.
   
   You should have received a copy of the GNU Lesser General Public
   License along with this program.  If not, see
   <http://www.gnu.org/licenses/>.

Usage
=====

.. function:: connect(url, username, password, [apptoken=None, hours=4])
              
   Connect to the QuickBase instance at *url* with the specified
   *username* & *password*.  *apptoken* is stored in the connection
   for future use, but is *not* validated against the QuickBase
   application.  If *hours* is given, then request that the returned
   ticket be valid for that many hours.  Returns an instance of the
   :class:`Connection` class.

   .. warning::

      *url* should be of the form 'https://example.quickbase.com/';
      future enhancement should use a URL library to Do the Right
      Thing.

.. class:: Connection

   A :class:`Connection` represents a persistent QuickBase connection.

   .. method:: do_query(dbid, [query=None, clist=None,
               slist=None, options={}, raw=False, fmt=None]):

      Execute `API_DoQuery
      <http://www.quickbase.com/api-guide/index.html#do_query.html>`_,
      by default returning a list of :class:`QuickBaseRecord`.  If the
      resulting reply is too big for QuickBase to return, it will
      split the result set in half and re-request, recursively.  This
      means that one shouldn't need to worry about too-large queries
      as a matter of course; note that it's more efficient to chunk
      the queries manually, as that will eliminate superfluous failed
      requests.

      *dbid*
      
         The QuickBase database ID.

      *query*
      
         The QuickBase query to execute With no *query*,
         :meth:`Connection.do_query()` will return all records in
         *dbid*.

         If *query* is an integer, then it represents a QuickBase
         query ID; otherwise, it's a string,
         e.g. ``"{'7'.EX.'Foobar'}"``.

      *clist*
      
         A QuickBase clist, i.e. a dot-delimited list of field IDs,
         e.g. ``'3.7.42'``.  *slist* is similar, but indicates the
         fields to sort by.

      *options*
      
         A dict representing the appropriate QuickBase options to
         pass; it is turned into a QuickBase option string via an
         arcane process (which is ripe for fixing).  If either
         ``'onlynew'`` or ``'nosort'`` is present, *even if its
         associated value is false*, then ``'onlynew'`` or
         ``'nosort'``, respectively, will be inserted into the option
         string.  All other keys and values will be inserted as
         hyphen-separated pairs.

      *raw*
      
         If ``True``, then :meth:`Connection.do_query()` returns the
         complete XML node structure as parsed by BeautifulSoup from
         the QuickBase response.  One should not normally need to do
         this, but it does come in handy sometimes when debugging
         particularly hairy issues.

   .. method:: do_query_count(dbid, query=None, raw=False):

      Execute `API_DoQueryCount
      <http://www.quickbase.com/api-guide/index.html#do_query_count.html>`_,
      by default returning an integer indicating the number of records
      which would be returned by *query*.  If *raw* is ``True``, then the
      raw XML node tree of the response will be returned instead.

   .. method:: add_record(dbid, record, raw=false):

      execute `api_addrecord
      <http://www.quickbase.com/api-guide/index.html#add_record.html>`_
      to add a new record to the quickbase table identified by *dbid*,
      returning a tuple containing the record id and update id of the
      new record, unless *raw* is ``true``, in which case the raw xml
      node tree of the response will be returned instead.

      *record* is a dict.  the keys are either integer field ids or
      string field names.  the values are either string data or
      :class:`File` instances.

   .. method:: edit_record(dbid, record_id, values, raw=False):

      Execute `API_EditRecord
      <http://www.quickbase.com/api-guide/index.html#edit_record.html>`_
      to edit an existing record with the record ID *record_id* in the
      QuickBase table identified by *dbid*, returning a tuple
      containing the number of fields changed and the new update ID of
      the record, unless *raw* is ``True``, in which case the raw XML
      node tree of the response will be returned instead.  *values* is
      a dict in the same format as *record* as for
      :meth:`Connection.edit_record()`.

   .. method:: delete_record(dbid, record_id, raw=False):

      Execute `API_DeleteRecord
      <http://www.quickbase.com/api-guide/index.html#delete_record.html>`_
      to delete record ID *record_id* from QuickBase table *dbid*,
      returning the record ID of the deleted record, unless *raw* is
      ``True``, in which case the raw XML node tree of the response
      will be returned instead.

   .. method:: run_import(dbid, import_id, raw=False):

      Execute `API_RunImport
      <http://www.quickbase.com/api-guide/index.html#runimport.html>`_
      to run a saved table-to-table import in Quickbase identified by
      *import_id*, returning the *import_status*, unless *raw* is
      ``True``, in which case the raw XML node tree of the response
      will be returned instead.
      :meth:`Connection.run_import()`.

   .. method:: import_from_csv(dbid, csv_file, clist, encoding='utf-8', skipfirst=True, raw=False, split=5000):

      Execute `API_ImportFromCSV
      <http://www.quickbase.com/api-guide/index.html#importfromcsv.html>`_
      to add or update records in QuickBase table *dbid*, by default
      returning a dict with the keys `num_recs_added`,
      `num_recs_input`, `num_recs_updated` and `records`; the first
      three are all integers and the last is a list of (record ID,
      update ID) tuples.  If *raw* is ``True``, then the raw XML node
      tree of the response will be returned instead.

      Since QuickBase can choke on too-large imports, *split*
      indicates how many records at a time should be uploaded.  Across
      the data we've normally been importing, 5,000 was a decent
      number; YMMV.

      *csv_file*
      
         An open file-like object to be passed to :func:`csv.reader()`.

      *clist*
      
         A standard QuickBase column list, used to indicate which
         fields are to be imported.

      *encoding*
      
         A Python encoding string (e.g. 'utf-8') used to decode the
         data after it's read in by :meth:`csv.reader.readlines()`.

      *skipfirst*
      
         Whether the first row of data in the CSV file should be
         skipped.  Should be set to ``False`` if one's CSV doesn't
         have a header line.

   .. method:: download(dbid, rid, fid, vid="0"):

      http://quickbase.intuit.com/developer/articles/downloading-files>`_
      to download an attached file in the Quickbase table identified
      by *dbid*, for the record ID *rid*, field ID *fid* and verion
      ID *vid*, where the default version ID of "0" downloads the
      latest version.
      :meth:`Connection.download()`.

   .. method:: user_roles(dbid, raw=False):

      Execute `API_UserRoles
      <http://www.quickbase.com/api-guide/index.html#userroles.html>`_
      to request the list of users and their roles in the QuickBase
      application identified by *dbid*, returning a list of users as
      dicts. If *raw* is ``True``, then the raw XML node tree of the
      reponse will be returned instead.
      :meth:`Connection.edit_record()`.

   .. method:: add_user_to_role(dbid, userid, roleid):

      Execute `API_AddUserToRole
      <http://www.quickbase.com/api-guide/index.html#add_user_to_role.html>`_
      to add a user with ID *userid* to the role with ID *roleid* for
      the Quickbase application identified by *dbid*.
      :meth:`Connection.add_user_to_role()`.

   .. method:: remove_user_from_role(dbid, userid, roleid):

      Execute `API_RemoveUserFromRole
      <http://www.quickbase.com/api-guide/index.html#removeuserfromrole.html>`_
      to remove a user with ID *userid* from the role with ID *roleid* for
      the Quickbase application identified by *dbid*.
      :meth:`Connection.remove_user_to_role()`.

   .. method:: get_schema(dbid, [raw=False]):

      Execute `API_GetSchema
      <http://www.quickbase.com/api-guide/index.html#getschema.html>`_,
      returning a :class:`TableInfo` object associated with QuickBase
      table *dbid*.  :meth:`Connection.get_schema()` can be given a
      *dbid* pointing to a single table or a full app. If the *dbid*
      passed is a table, the response will contain a list of fields,
      among other info. If the *dbid* passed is an app, the response
      will contain a list of chdbids (child dbids), but will not be
      useful as a :class:`TableInfo` object, and thus must be given
      *raw* = ``True`` if the intent is to access the chdbid info.

      *dbid*
      
         The QuickBase database ID.

      *raw*
      
         If ``True``, then :meth:`Connection.get_schema()` returns the
         complete XML node structure as parsed by BeautifulSoup from
         the QuickBase response.

.. class:: TableInfo

   A representation of the QuickBase table that makes schema data
   easily accessible.

.. class:: QuickBaseRecord

   A :class:`QuickBaseRecord` represents a single QuickBase record.
   It's a dict-like object which allows accessing fields as both items
   and attributes, although it doesn't implement :meth:`iterkeys()`.
   Each QuickBase field is accessible with its field label,
   e.g. ``record.record_id_`` or ``record['record_id_']`` will both be
   the 'Record Id#' field.  There is also a special field _fields,
   which records the record's data.

   .. warning::

      QuickBase allows the definition of multiple fields with
      different names but the same label, e.g. two fields named
      :samp:`foo+` and :samp:`foo*` will have the same label :samp:`foo_`.
      :class:`QuickBaseRecord` does not support this.  A future
      enhancement should allow accessing fields by name as well as
      label using the dict-like syntax.

.. class:: File(filename, data)

   Files have to be uploaded to QuickBase specially.  The path of least
   resistance was create a special class whose instance are recognized
   by :meth:`Connection:add_record()` and
   :meth:`Connection:edit_record()`.  Use by attaching it as one of
   the values in an add or edit dict.

   *filename* is the filename as it will appear in QuickBase.

   *data* is a string containing the contents of the file, as they
   will be uploaded to QuickBase.
