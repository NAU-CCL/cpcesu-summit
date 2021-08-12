from django.views import View
from django.http import HttpResponse
from django.template.loader import render_to_string


# A class based view for serving the results of a database query in the form of
# a table of objects and their fields.
# It will return rendered HTML which can be easily slotted into an existing modal.
class GenericQueryModal(View):

    # The path to the template which will be rendered and returned; by default
    # the template will have a list of objects and a list of fields in its context
    template_name = "generic_query_modal.html"
    # The list of fields to be retreived and displayed from the queryset retreived
    # by get_queryset; by default returned by get_fields
    fields = []
    # The optional list of custom names for the columns of the table; by
    # default returned by get_field_names
    field_names = []
    # The optional string which defines the URL rows in the table should
    # link to; if static_link is given a value it will be used instead of other
    # links
    static_link = None
    # The optional string which defines a URL with %s placeholders for values from
    # the objects returned by get_queryset; rows in the table will link
    # to a URL based on these values; by default returned by get_link_base
    link_base = None
    # The ordered list of fields to be considered for the URL; this list should
    # have the same number of elements as there are %s in link_base; this list
    # of fields does not need to be the same as fields; by default returned by
    # get_link_fields
    link_fields = []
    # For example:
    # link_base = "/partners/p/%s"
    # link_fields = ["name"]
    # would result in each item in the returned table linking to the corresponding
    # partner page for that item's name

    # The optional boolean which, if set to true, will add another column to the
    # returned table which links to the URL defined by link_base and link_fields;
    # also, the rows in the table will not link to anything when this is true
    link_as_column = False

    # The optional string which defines the JS function rows in the table
    # should call when clicked; if static_onclick is given a value it will be used
    # instead of other onclick functions
    static_onclick = None
    # The optional string which defines a JS function call with %s placeholders
    # for values from the objects returned by get_queryset; rows in the table
    # will call the function based on this values when clicked; by default
    # returned by get_onclick_base
    onclick_base = None
    # The optional list of fields to be considered for the function call; this list
    # should have the same number of elements as there are %s in onclick_base;
    # this list of fields does not need to be the same as fields; by default
    # returned by get_onclick_fields
    onclick_fields = []
    # For example:
    # onclick_base = "openPartnerDetails(partner_id=%s)"
    # onclick_fields = ["id"]
    # would result in each item in the returned table, when clicked, calling the
    # openPartnerDetails function and pass it that item's id

    # The optional string which defines a JS function to call when the new button
    # above the table of items is clicked
    new_onclick = None

    # An optional string which defines the field of the queryset to be considered
    # by a basic search bar; this search bar compares the string entered into the
    # text field against the field
    search_field = None



    # Using the queryset and set of fields returned by the get_queryset and get_fields
    # parse the queryset returned by get_queryset into a list of dictionaries and
    # pass that, and the set of fields to the template. Render the template and
    # return the resulting HTML
    # This method is not intended to be overridden
    def get(self, request, *args, **kwargs):
        context = {}
        try:
            fields = self.get_fields( request, *args, **kwargs)
            objects = self.get_queryset( request, *args, **kwargs )
            object_list = [ { field : getattr( object, field, None ) for field in fields } for object in objects ]
            context["objects"] = object_list

            field_names = self.get_field_names( request, *args, **kwargs )
            if field_names and len(fields) == len(field_names):
                context["fields"] = field_names
            else:
                context["fields"] = fields

            link_base = self.get_link_base( request, *args, **kwargs )
            link_fields = self.get_link_fields( request, *args, **kwargs )
            if self.static_link is not None:
                for object in context["objects"]:
                    object["link"] = self.static_link
                context["links"] = True
            elif link_base and link_fields:
                link_list = [ link_base % tuple( getattr( object, field, None ) for field in link_fields ) for object in objects ]
                for object, link in zip( context["objects"], link_list ):
                    object["link"] = link
                context["links"] = True
            else:
                context["links"] = False

            context["link_as_column"] = self.get_link_as_column( request, *args, **kwargs )

            onclick_base = self.get_onclick_base( request, *args, **kwargs )
            onclick_fields = self.get_onclick_fields( request, *args, **kwargs )
            if self.static_onclick is not None:
                for object in context["objects"]:
                    object["link"] = self.static_onclick
                context["onclick"] = True
            elif onclick_base and onclick_fields:
                print( onclick_base )
                print( onclick_fields )
                onclick_list = [ onclick_base % tuple( getattr( object, field, None ) for field in onclick_fields ) for object in objects ]
                for object, onclick in zip( context["objects"], onclick_list ):
                    object["onclick"] = onclick
                context["onclick"] = True
            else:
                context["onclick"] = False


            context["new_onclick"] = self.get_new_onclick( request, *args, **kwargs )


            context["search_field"] = self.get_search_field( request, *args, **kwargs )
        except Exception as e:
            # TODO: Expand upon context["error"] to have the modal display greater
            # details about what specifically went wrong
            print(e)
            context["error"] = True
            context["objects"] = None
            context["fields"] = None
            context["links"] = None
            context["onclick"] = None
            context["new_onclick"] = None
            context["search_field"] = None
        context["error"] = False
        return HttpResponse( render_to_string( self.template_name, context ) )

    # Intended to be overriden by the class that extends GenericQueryModal to return
    # the desired queryset to be displayed
    def get_queryset(self, request, *args, **kwargs):
        return None

    # Optional; Returns the list of fields to be retrieved and displayed from
    # the queryset returned by get_queryset
    def get_fields(self, request, *args, **kwargs):
        return self.fields

    # Optional; Returns a list of custom names for the columns of the returned HTML;
    # If get_field_names does not return a list of the same length as that returned
    # by get_fields, the strings returned by get_fields will be used as the column
    # names
    def get_field_names(self, request, *args, **kwargs):
        return self.field_names

    # Optional; returns a string which defines a URL; may include %s placeholders
    # to be filled in with values from fields as defined by get_link_fields
    def get_link_base(self, request, *args, **kwargs):
        return self.link_base

    # Optional; Returns a list of field names which correspond to the fields of the
    # objects returned by get_queryset to be slotted into the %s of the link base;
    # must return a list with the same number of items as the link base has %s
    def get_link_fields(self, request, *args, **kwargs):
        return self.link_fields

    # Optional; Return whether or not the table rows, or a seperate column,
    # should link to the URL defined by get_link_base and get_link_fields
    def get_link_as_column(self, request, *args, **kwargs):
        return self.link_as_column

    # Optional; Returns a string which defines a JS function call; may include %s
    # placeholders to be filled in with values from fields as defined by get_onclick_fields
    def get_onclick_base(self, request, *args, **kwargs):
        return self.onclick_base

    # Optional; Returns a list of field names which correspond to the fields of the
    # objects returned by get_queryset to be slotted into the %s of the onclick base;
    # must return a list with the same number of items as the link base has %s
    def get_onclick_fields(self, request, *args, **kwargs):
        return self.onclick_fields

    # Optional; Returns a string which defines a JS function call to be called
    # when the new button above the table is clicked
    def get_new_onclick(self, request, *args, **kwargs):
        return self.new_onclick

    # Optional; Returns a single field name which defines the field of the
    # queryset to be considered by a basic search bar; this search bar compares
    # the string entered into the text field against the field
    def get_search_field(self, request, *args, **kwargs):
        return self.search_field