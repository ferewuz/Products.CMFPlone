from Products.CMFDefault.DiscussionTool import DiscussionTool as BaseTool
from Products.CMFPlone import ToolNames
from AccessControl import ClassSecurityInfo
from Globals import InitializeClass
from Products.CMFPlone.PloneBaseTool import PloneBaseTool
from Products.CMFDefault.permissions import ReplyToItem

from StructuredText.StructuredText import HTML
from DocumentTemplate.DT_Util import html_quote

from Acquisition import aq_base
from Products.CMFCore.interfaces.Discussions \
        import DiscussionResponse as IDiscussionResponse

class DiscussionTool(PloneBaseTool, BaseTool):

    meta_type = ToolNames.DiscussionTool
    security = ClassSecurityInfo()
    toolicon = 'skins/plone_images/discussionitem_icon.gif'

    __implements__ = (PloneBaseTool.__implements__, BaseTool.__implements__, )

    security.declareProtected(ReplyToItem, 'cookReply')
    def cookReply(self, reply, text_format=None):
        """ TODO We need this because currently we can not easily change the
            text_format on document objects.  Discussions in plone are going
            to use plain-text for now.  stx is too confusing.
        """
        level = reply._stx_level
        text = reply.text

        if text_format is None:
            text_format=reply.text_format

        if text_format == 'html':
            reply.text = reply.cooked_text = text
        elif text_format == 'plain':
            reply.text = text
            reply.cooked_text = html_quote(text).replace('\n','<br>')
        else:
            reply.cooked_text = HTML(text=text, level=level)
            reply.text = text

DiscussionTool.__doc__ = BaseTool.__doc__

InitializeClass(DiscussionTool)
