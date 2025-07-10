# llmport/magic.py
import importlib

def load_ipython_extension(ipython):
    """
    Loads the llmport magic command for IPython.
    This function is called by IPython when the extension is loaded.
    """
    try:
        from IPython.core.magic import register_cell_magic
        # Import your core functions
        from . import llmport as llmport_func
        from . import update as update_func

        @register_cell_magic
        def llmport(line, cell):
            """
            %%llmport <module_name>
            <prompt>
            
            Generates and automatically imports the module into the current session.
            """
            module_name = line.strip()
            prompt = cell.strip()
            
            if not module_name:
                print("❌ Usage: %%llmport <module_name>")
                return
            
            try:
                # 1. Call your existing function to generate the .py file
                print(f"✨ Generating module '{module_name}'...")
                module = llmport_func(module_name, prompt)

                if module:
                    # 2. Inject the module object into the user's interactive namespace
                    ipython.user_ns[module_name] = module
                    print(f"✅ Success! Module '{module_name}' was generated and imported.")
                else:
                    print(f"❌ Failed to import module '{module_name}'. See error above.")

            except Exception as e:
                print(f"❌ An error occurred: {e}")

        @register_cell_magic
        def llmupdate(line, cell):
            """
            %%llmupdate <module_name>
            <prompt>
            
            Updates an existing module and reloads it in the current session.
            """
            module_name = line.strip()
            prompt = cell.strip()
            
            if not module_name:
                print("❌ Usage: %%llmupdate <module_name>")
                return
            
            try:
                print(f"✨ Updating module '{module_name}'...")
                module = update_func(module_name, prompt)
                
                if module:
                    # Inject the module object into the user's interactive namespace
                    ipython.user_ns[module_name] = module
                    print(f"✅ Success! Module '{module_name}' was updated and reloaded.")
                else:
                    print(f"❌ Failed to reload module '{module_name}'. See error above.")

            except Exception as e:
                print(f"❌ An error occurred: {e}")

    except ImportError:
        # This part remains the same
        print("IPython is not installed. The %%llmport magic command is not available.")
