This example shows how to provide a list of runtime Database Names for an AVR for .NET Web application that are automatically iterated. The first Database Name in the list that connects successfully is the Database Name used at runtime. 

> [See full annotated code for this example here.](https://asna.github.io/database-name-search/pycco-index.html)    


#### Define your Database Name list

The list of Database Names you want iterated is stored in a DBNames `appSettings` as shown below in Figure 1. 

    <?xml version="1.0"?>

    <configuration>
    <appSettings>
        <add key="DBNames" value="*Public/CypressNCP,*Public/DG NET Local"/>
        <!--<add key="DBNameOverride" value="*Public/DG16-DG160X"/>-->
    </appSettings>
    <system.web>
        <compilation debug="true" targetFramework="4.5.2"/>
    </system.web>
    </configuration>

<small>Figure 1. Example `web.config` with `DBNames` and `DBNameOverride` keys.

Assign the comma-separated DataBase Names you want used, in the order you want them used, in the `DBNames` key. The code attempts to connect with each DataBase Name, starting with the first one. The first DataBase Name that connects successfully is used. 

If you want to temporarily override the `DBNames` list, provide a Database Name with the `DBNameOverride` key. (This key is provided in the example `web.config` above but is commented out) This Database Name, and only this Database Name, will be used be used at runtime. If this Database Name fails to connect, the application will not work. 

#### Connecting your app at run time

Declare your app's Database Name like you always would, as shown below. 

    DclDB DGDB DBName('*Public/DG Net Local') 
    DclFld dg Type(DataGateDB) New()

> [See the DBName class annotated code.](https://asna.github.io/database-name-search/App_Code/datagatedb.vr.html)    

The DataBase named provided here used is at compile-time. At runtime, the `DataGateDB` class uses the information in the `web.config` keys to attempt to connect to a runtime Database Name. The code below uses `DataGateDB's` `AttemptConnection` method to iterate the Database Name list you provided in `web.config` (or use the DataBase Name override if provided).

    pgmDB = dg.AttemptConnection()
    If pgmDB <> *Nothing 
        // No connections succeeded.
    Else
        // A connection succeeded.
    EndIf 

<small>Figure 2a. Attempt to create a connection with the list of Database Names provided.</small>

If, after calling `AttemptConnection` the `pgmDB` object is `*Nothing` then none of the Database Names provided could connect. Your program can use the state of the `pgmDB` object to determine what to do if all of the connections fail. When `AttemptConnection` succeeds, it returns an open ASNA DataGate connection.

The `AttemptConnection` method calls the `GetNewConnection` which is the method provided to attempt to create a connection. 

If needed, you can also call `GetNewConnection` directly. Doing that, you could connect to a specific Database Name as shown below:

    DclDB pgmDB 

    ...

    pgmDB = dg.GetNewConnection('*Public/DG NET Local') 

<small>Figure 2b. Attempt to create a connection with a specific Database Name.</small>

A log of all connection activity is available in the `DataGateDB's` `Log` property. By default each line in this log ends with a `<br>` tag so that is easy to display with HTML. If you'd rather have each line in the log end with a carriage return and line feed, set `DataGateDB's` `LogWithBRTag` to *False before calling `AttemptConnection`.  

    Attempting connection with Database Name *Public/CypressNCP
    *Public/CypressNCP connection error: No connection could be made because the target machine actively refused it 10.1.3.207:5188
    Attempting connection with Database Name *Public/DG NET Local
    Successfully connected with Database Name *Public/DG NET Local

<small>Figure 3. Example log contents.</small>



