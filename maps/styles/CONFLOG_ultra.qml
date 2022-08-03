<!DOCTYPE qgis PUBLIC 'http://mrcc.com/qgis.dtd' 'SYSTEM'>
<qgis hasScaleBasedVisibilityFlag="0" minScale="1e+08" version="3.24.1-Tisler" styleCategories="AllStyleCategories" maxScale="0">
  <flags>
    <Identifiable>1</Identifiable>
    <Removable>1</Removable>
    <Searchable>1</Searchable>
    <Private>0</Private>
  </flags>
  <temporal enabled="0" fetchMode="0" mode="0">
    <fixedRange>
      <start></start>
      <end></end>
    </fixedRange>
  </temporal>
  <customproperties>
    <Option type="Map">
      <Option type="bool" value="false" name="WMSBackgroundLayer"/>
      <Option type="bool" value="false" name="WMSPublishDataSourceUrl"/>
      <Option type="int" value="0" name="embeddedWidgets/count"/>
      <Option type="QString" value="Value" name="identify/format"/>
    </Option>
  </customproperties>
  <pipe-data-defined-properties>
    <Option type="Map">
      <Option type="QString" value="" name="name"/>
      <Option name="properties"/>
      <Option type="QString" value="collection" name="type"/>
    </Option>
  </pipe-data-defined-properties>
  <pipe>
    <provider>
      <resampling enabled="false" maxOversampling="2" zoomedOutResamplingMethod="nearestNeighbour" zoomedInResamplingMethod="nearestNeighbour"/>
    </provider>
    <rasterrenderer classificationMax="15000" band="1" nodataColor="" opacity="1" type="singlebandpseudocolor" alphaBand="-1" classificationMin="0">
      <rasterTransparency/>
      <minMaxOrigin>
        <limits>None</limits>
        <extent>WholeRaster</extent>
        <statAccuracy>Estimated</statAccuracy>
        <cumulativeCutLower>0.02</cumulativeCutLower>
        <cumulativeCutUpper>0.98</cumulativeCutUpper>
        <stdDevFactor>2</stdDevFactor>
      </minMaxOrigin>
      <rastershader>
        <colorrampshader maximumValue="15000" minimumValue="0" labelPrecision="4" clip="0" colorRampType="INTERPOLATED" classificationMode="1">
          <colorramp type="gradient" name="[source]">
            <Option type="Map">
              <Option type="QString" value="68,1,84,191" name="color1"/>
              <Option type="QString" value="253,231,37,191" name="color2"/>
              <Option type="QString" value="ccw" name="direction"/>
              <Option type="QString" value="0" name="discrete"/>
              <Option type="QString" value="gradient" name="rampType"/>
              <Option type="QString" value="rgb" name="spec"/>
              <Option type="QString" value="0.0196078;70,8,92,191;rgb;ccw:0.0392157;71,16,99,191;rgb;ccw:0.0588235;72,23,105,191;rgb;ccw:0.0784314;72,29,111,191;rgb;ccw:0.0980392;72,36,117,191;rgb;ccw:0.117647;71,42,122,191;rgb;ccw:0.137255;70,48,126,191;rgb;ccw:0.156863;69,55,129,191;rgb;ccw:0.176471;67,61,132,191;rgb;ccw:0.196078;65,66,135,191;rgb;ccw:0.215686;63,72,137,191;rgb;ccw:0.235294;61,78,138,191;rgb;ccw:0.254902;58,83,139,191;rgb;ccw:0.27451;56,89,140,191;rgb;ccw:0.294118;53,94,141,191;rgb;ccw:0.313725;51,99,141,191;rgb;ccw:0.333333;49,104,142,191;rgb;ccw:0.352941;46,109,142,191;rgb;ccw:0.372549;44,113,142,191;rgb;ccw:0.392157;42,118,142,191;rgb;ccw:0.411765;41,123,142,191;rgb;ccw:0.431373;39,128,142,191;rgb;ccw:0.45098;37,132,142,191;rgb;ccw:0.470588;35,137,142,191;rgb;ccw:0.490196;33,142,141,191;rgb;ccw:0.509804;32,146,140,191;rgb;ccw:0.529412;31,151,139,191;rgb;ccw:0.54902;30,156,137,191;rgb;ccw:0.568627;31,161,136,191;rgb;ccw:0.588235;33,165,133,191;rgb;ccw:0.607843;36,170,131,191;rgb;ccw:0.627451;40,174,128,191;rgb;ccw:0.647059;46,179,124,191;rgb;ccw:0.666667;53,183,121,191;rgb;ccw:0.686275;61,188,116,191;rgb;ccw:0.705882;70,192,111,191;rgb;ccw:0.72549;80,196,106,191;rgb;ccw:0.745098;90,200,100,191;rgb;ccw:0.764706;101,203,94,191;rgb;ccw:0.784314;112,207,87,191;rgb;ccw:0.803922;124,210,80,191;rgb;ccw:0.823529;137,213,72,191;rgb;ccw:0.843137;149,216,64,191;rgb;ccw:0.862745;162,218,55,191;rgb;ccw:0.882353;176,221,47,191;rgb;ccw:0.901961;189,223,38,191;rgb;ccw:0.921569;202,225,31,191;rgb;ccw:0.941176;216,226,25,191;rgb;ccw:0.960784;229,228,25,191;rgb;ccw:0.980392;241,229,29,191;rgb;ccw" name="stops"/>
            </Option>
            <prop k="color1" v="68,1,84,191"/>
            <prop k="color2" v="253,231,37,191"/>
            <prop k="direction" v="ccw"/>
            <prop k="discrete" v="0"/>
            <prop k="rampType" v="gradient"/>
            <prop k="spec" v="rgb"/>
            <prop k="stops" v="0.0196078;70,8,92,191;rgb;ccw:0.0392157;71,16,99,191;rgb;ccw:0.0588235;72,23,105,191;rgb;ccw:0.0784314;72,29,111,191;rgb;ccw:0.0980392;72,36,117,191;rgb;ccw:0.117647;71,42,122,191;rgb;ccw:0.137255;70,48,126,191;rgb;ccw:0.156863;69,55,129,191;rgb;ccw:0.176471;67,61,132,191;rgb;ccw:0.196078;65,66,135,191;rgb;ccw:0.215686;63,72,137,191;rgb;ccw:0.235294;61,78,138,191;rgb;ccw:0.254902;58,83,139,191;rgb;ccw:0.27451;56,89,140,191;rgb;ccw:0.294118;53,94,141,191;rgb;ccw:0.313725;51,99,141,191;rgb;ccw:0.333333;49,104,142,191;rgb;ccw:0.352941;46,109,142,191;rgb;ccw:0.372549;44,113,142,191;rgb;ccw:0.392157;42,118,142,191;rgb;ccw:0.411765;41,123,142,191;rgb;ccw:0.431373;39,128,142,191;rgb;ccw:0.45098;37,132,142,191;rgb;ccw:0.470588;35,137,142,191;rgb;ccw:0.490196;33,142,141,191;rgb;ccw:0.509804;32,146,140,191;rgb;ccw:0.529412;31,151,139,191;rgb;ccw:0.54902;30,156,137,191;rgb;ccw:0.568627;31,161,136,191;rgb;ccw:0.588235;33,165,133,191;rgb;ccw:0.607843;36,170,131,191;rgb;ccw:0.627451;40,174,128,191;rgb;ccw:0.647059;46,179,124,191;rgb;ccw:0.666667;53,183,121,191;rgb;ccw:0.686275;61,188,116,191;rgb;ccw:0.705882;70,192,111,191;rgb;ccw:0.72549;80,196,106,191;rgb;ccw:0.745098;90,200,100,191;rgb;ccw:0.764706;101,203,94,191;rgb;ccw:0.784314;112,207,87,191;rgb;ccw:0.803922;124,210,80,191;rgb;ccw:0.823529;137,213,72,191;rgb;ccw:0.843137;149,216,64,191;rgb;ccw:0.862745;162,218,55,191;rgb;ccw:0.882353;176,221,47,191;rgb;ccw:0.901961;189,223,38,191;rgb;ccw:0.921569;202,225,31,191;rgb;ccw:0.941176;216,226,25,191;rgb;ccw:0.960784;229,228,25,191;rgb;ccw:0.980392;241,229,29,191;rgb;ccw"/>
          </colorramp>
          <item label="0,0000" color="#440154" alpha="191" value="0"/>
          <item label="294,1170" color="#46085c" alpha="191" value="294.117"/>
          <item label="588,2355" color="#471063" alpha="191" value="588.2355"/>
          <item label="882,3525" color="#481769" alpha="191" value="882.3525"/>
          <item label="1176,4710" color="#481d6f" alpha="191" value="1176.471"/>
          <item label="1470,5880" color="#482475" alpha="191" value="1470.5880000000002"/>
          <item label="1764,7050" color="#472a7a" alpha="191" value="1764.705"/>
          <item label="2058,8250" color="#46307e" alpha="191" value="2058.825"/>
          <item label="2352,9450" color="#453781" alpha="191" value="2352.945"/>
          <item label="2647,0650" color="#433d84" alpha="191" value="2647.065"/>
          <item label="2941,1700" color="#414287" alpha="191" value="2941.17"/>
          <item label="3235,2900" color="#3f4889" alpha="191" value="3235.29"/>
          <item label="3529,4100" color="#3d4e8a" alpha="191" value="3529.41"/>
          <item label="3823,5300" color="#3a538b" alpha="191" value="3823.53"/>
          <item label="4117,6500" color="#38598c" alpha="191" value="4117.65"/>
          <item label="4411,7700" color="#355e8d" alpha="191" value="4411.7699999999995"/>
          <item label="4705,8750" color="#33638d" alpha="191" value="4705.875"/>
          <item label="4999,9950" color="#31688e" alpha="191" value="4999.995"/>
          <item label="5294,1150" color="#2e6d8e" alpha="191" value="5294.115"/>
          <item label="5588,2350" color="#2c718e" alpha="191" value="5588.235000000001"/>
          <item label="5882,3550" color="#2a768e" alpha="191" value="5882.355"/>
          <item label="6176,4750" color="#297b8e" alpha="191" value="6176.474999999999"/>
          <item label="6470,5950" color="#27808e" alpha="191" value="6470.595"/>
          <item label="6764,7000" color="#25848e" alpha="191" value="6764.7"/>
          <item label="7058,8200" color="#23898e" alpha="191" value="7058.82"/>
          <item label="7352,9400" color="#218e8d" alpha="191" value="7352.9400000000005"/>
          <item label="7647,0600" color="#20928c" alpha="191" value="7647.06"/>
          <item label="7941,1800" color="#1f978b" alpha="191" value="7941.18"/>
          <item label="8235,3000" color="#1e9c89" alpha="191" value="8235.3"/>
          <item label="8529,4050" color="#1fa188" alpha="191" value="8529.405"/>
          <item label="8823,5250" color="#21a585" alpha="191" value="8823.525"/>
          <item label="9117,6450" color="#24aa83" alpha="191" value="9117.645"/>
          <item label="9411,7650" color="#28ae80" alpha="191" value="9411.765"/>
          <item label="9705,8850" color="#2eb37c" alpha="191" value="9705.885"/>
          <item label="10000,0050" color="#35b779" alpha="191" value="10000.005000000001"/>
          <item label="10294,1250" color="#3dbc74" alpha="191" value="10294.125"/>
          <item label="10588,2300" color="#46c06f" alpha="191" value="10588.23"/>
          <item label="10882,3500" color="#50c46a" alpha="191" value="10882.35"/>
          <item label="11176,4700" color="#5ac864" alpha="191" value="11176.470000000001"/>
          <item label="11470,5900" color="#65cb5e" alpha="191" value="11470.59"/>
          <item label="11764,7100" color="#70cf57" alpha="191" value="11764.71"/>
          <item label="12058,8300" color="#7cd250" alpha="191" value="12058.83"/>
          <item label="12352,9350" color="#89d548" alpha="191" value="12352.935"/>
          <item label="12647,0550" color="#95d840" alpha="191" value="12647.055"/>
          <item label="12941,1750" color="#a2da37" alpha="191" value="12941.175"/>
          <item label="13235,2950" color="#b0dd2f" alpha="191" value="13235.295"/>
          <item label="13529,4150" color="#bddf26" alpha="191" value="13529.415"/>
          <item label="13823,5350" color="#cae11f" alpha="191" value="13823.535"/>
          <item label="14117,6400" color="#d8e219" alpha="191" value="14117.64"/>
          <item label="14411,7600" color="#e5e419" alpha="191" value="14411.76"/>
          <item label="14705,8800" color="#f1e51d" alpha="191" value="14705.880000000001"/>
          <item label="15000,0000" color="#fde725" alpha="191" value="15000"/>
          <rampLegendSettings useContinuousLegend="1" maximumLabel="" suffix="" prefix="" direction="0" orientation="1" minimumLabel="">
            <numericFormat id="basic">
              <Option type="Map">
                <Option type="QChar" value="" name="decimal_separator"/>
                <Option type="int" value="6" name="decimals"/>
                <Option type="int" value="0" name="rounding_type"/>
                <Option type="bool" value="false" name="show_plus"/>
                <Option type="bool" value="true" name="show_thousand_separator"/>
                <Option type="bool" value="false" name="show_trailing_zeros"/>
                <Option type="QChar" value="" name="thousand_separator"/>
              </Option>
            </numericFormat>
          </rampLegendSettings>
        </colorrampshader>
      </rastershader>
    </rasterrenderer>
    <brightnesscontrast contrast="0" brightness="0" gamma="1"/>
    <huesaturation grayscaleMode="0" invertColors="0" colorizeOn="0" colorizeRed="255" colorizeGreen="128" colorizeStrength="100" colorizeBlue="128" saturation="0"/>
    <rasterresampler maxOversampling="2"/>
    <resamplingStage>resamplingFilter</resamplingStage>
  </pipe>
  <blendMode>0</blendMode>
</qgis>
