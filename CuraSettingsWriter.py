from UM.Application import Application
from UM.Preferences import Preferences
from UM.Settings.ContainerRegistry import ContainerRegistry
from UM.Workspace.WorkspaceWriter import WorkspaceWriter


import UM.Settings.SettingRelation

class CuraSettingsWriter(WorkspaceWriter):
   
    def write(self, stream, nodes, mode):
        stream.write("<style>")
        stream.write(" .category { font-size:1.5em; } ")
        stream.write(" .off { background-color:grey; } ")
        stream.write(" .valueCol { width:200px;text-align:right }")
        stream.write("</style>")
        
        application = Application.getInstance()
        machine_manager = application.getMachineManager()        
        stack = application.getGlobalContainerStack()

        global_stack = machine_manager.activeMachine


        #jquery = open("plugins/plugins/CuraSettingsWriter/jquery-3.3.1.min.js","r", encoding="utf-8")
        
        stream.write("<script src='https://code.jquery.com/jquery-3.3.1.slim.min.js'></script>\n")
        stream.write("""<script>
                            $(document).ready(function(){
                                    $("#enabled").on("click",toggleDisabled);

                            });

                            function toggleDisabled(){
                                    $("tr.disabled").toggle();
                            }
                        </script>
                        <h1>Cura Settings Export</h1>
                        <button id='enabled'>Toggle Disabled</button><P>""")


        stream.write("<table width=50% border=1 cellpadding=3>")

        self._doTree(global_stack,"resolution",stream,0)
        self._doTree(global_stack,"shell",stream,0)
        self._doTree(global_stack,"infill",stream,0)
        self._doTree(global_stack,"material",stream,0)
        self._doTree(global_stack,"speed",stream,0)
        self._doTree(global_stack,"travel",stream,0)

        self._doTree(global_stack,"cooling",stream,0)
        self._doTree(global_stack,"support",stream,0)
        self._doTree(global_stack,"platform_adhesion",stream,0)
        self._doTree(global_stack,"meshfix",stream,0)
        self._doTree(global_stack,"blackmagic",stream,0)
        self._doTree(global_stack,"experimental",stream,0)
        self._doTree(global_stack,"dual",stream,0)
        self._doTree(global_stack,"machine_settings",stream,0)

        # for key in global_stack.getAllKeys():
        #     if global_stack.getProperty(key,"enabled") == True:
        #         if global_stack.getProperty(key,"type") == "category":
        #             self._doTree(global_stack,key,stream,0)

        stream.write("</table>")
        return True



    def _doTree(self,stack,key,stream,depth):   
        #output node
        if stack.getProperty(key,"type") == "category":
            stream.write("<tr>")
            stream.write("<td class=category colspan=3>" + str(stack.getProperty(key,"label")) + "</td>")
            #stream.write("<td class=category>" + str(key) + "</td>")
            stream.write("</tr>\n")
        else:
            style = "ok"    
            if stack.getProperty(key,"enabled") == False:
                style = "off"
                stream.write("<tr class=disabled>")
            else:
                stream.write("<tr>")
            stream.write("<td class="+style+" style='width:50%;padding-left:"+str(depth*25)+"'>" + str(stack.getProperty(key,"label")) + "</td>")
            stream.write("<td class='"+style+" valueCol'>" + str(stack.getProperty(key,"value")) + "</td>")
            stream.write("<td class="+style+" >" + str(stack.getProperty(key,"unit")) + "</td>")
            #stream.write("<td>" + str(stack.getProperty(key,"comments")) + "</td>")
            #stream.write("<td>" + str(stack.getProperty(key,"type")) + "</td>")
            stream.write("</tr>\n")

        #look for children
        if len(stack.getSettingDefinition(key).children) > 0:
            for i in stack.getSettingDefinition(key).children:       
                self._doTree(stack,i.key,stream,depth+1)
                    
                   
